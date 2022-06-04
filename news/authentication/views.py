import json
from django.conf import settings
from django.shortcuts import redirect, render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from .models import User
from django.core.cache import cache
from .forms import UserForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in


class CreateUserAPIView(APIView):
    """
    API class responsible for creating a user
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        user['posts_info'] = "{}"
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutUserAPIView(APIView):
    """
    API class that removes the token cookie from the user's logout web browser
    """
    permission_classes = (AllowAny, )
    def post(self, request):
        response = redirect('http://0.0.0.0:8000/')
        response.delete_cookie('token')
        return response
        

class AuthenticateUserAPIView(APIView):
    """
    API class that takes login data and returns a pair of tokens
    """
    permission_classes = (AllowAny, )
    def post(self, request):

        try:
            username = request.data["username"]
            password = request.data["password"]

            user = User.objects.get(username=username, password=password)
            if user:
                try:
                
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    user_details = {}
                    user_details["username"] = "%s" % (user.username)
                    user_details["token"] = token
                    user_details["refresh_token"] = str(refresh)
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    response = Response(user_details, status=status.HTTP_200_OK)               
                    return response

                except Exception as e:
                    raise e
            else:
                res = {
                    "error": "can not authenticate with the given credentials or the account has been deactivated"
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {"error": "please provide a username and a password"}
            return Response(res)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    The API class that modifies/shows user data takes a JWT token and when the data changes, PostSerializer().data
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get("user", {})

        serializer = UserSerializer(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveUserAPIView(APIView):
    """
    API class that deletes and logs out the user
    """
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        request.user.delete()
        response = redirect('http://0.0.0.0:8000/')
        response.delete_cookie('token')
        return response


@permission_classes(AllowAny,)
def RegisterView(request):
    error = ''

    if request.method == 'POST':
        form = UserForm(request.POST)
        
        username = form.data.get('username')
        email = form.data.get('email')
        password = form.data.get('password')

        body = {
            "email":email,
            "username":username,
            "password":password,
        }
        headers = {'content-type': 'application/json'}

        body = json.dumps(body)
        create_req = requests.post('http://0.0.0.0:8000/auth/api/create/',data=body,headers=headers)
        
        body = {
            "username":username,
            "password":password,
        }
        headers = {'content-type': 'application/json'}

        body = json.dumps(body)
        sign_req = requests.post('http://0.0.0.0:8000/auth/api/signin/',data=body,headers=headers)
        if sign_req.status_code == 200:
            return redirectWithCookies('http://0.0.0.0:8000/profile/',"token", json.loads(sign_req.text)['token'])
        else:
            error = 'invalid login or password'
        
    form = UserForm()

    data = {
        'form':form,
        'error':error
    }
    
    return render(request, 'auth/register.html', data)

@permission_classes(AllowAny,)
def SignInView(request):
    error = ''

    if request.method == 'POST':
        form = UserForm(request.POST)
        
        username = form.data.get('username')
        password = form.data.get('password')
        
        body = {
            "username":username,
            "password":password,
        }
        headers = {'content-type': 'application/json'}

        body = json.dumps(body)
        sign_req = requests.post('http://0.0.0.0:8000/auth/api/signin/',data=body,headers=headers)
        
        if sign_req.status_code == 200:
            return redirectWithCookies('http://0.0.0.0:8000/profile/',"token", json.loads(sign_req.text)['token'])
        else:
            error = 'invalid login or password'

    form = UserForm()

    data = {
        'form':form,
        'error':error
    }

    return render(request, 'auth/signin.html', data)

def EditUserView(request, username):

    if request.COOKIES.get("token") == None:
        return redirect('http://0.0.0.0:8000/')
    if requests.get('http://0.0.0.0:8000/auth/api/update/',headers={'Authorization':'Bearer '+request.COOKIES.get('token')}).status_code != 200:
        return redirect('http://0.0.0.0:8000/')
    error = ''

    user = User.objects.get(username=username)

    serializer_data = UserSerializer(user).data

    if request.method == 'POST':
        form = User(request.POST)
        serializer_data['username'] = form.data.get('username')
        serializer_data['password'] = form.data.get('password')
        serializer_data['email'] = form.data.get('email')

        update_req = requests.put('http://0.0.0.0:8000/auth/api/update/', data = serializer_data,
         headers={'content-type':'application/json', 'Authorization':'Bearer ' + request.COOKIES.get('token')})

        if update_req.status_code == 200:
            redirectWithCookies('http://0.0.0.0:8000/profile/'+serializer_data['username'],'token',request.COOKIES.get('token'))
        else:
            error = 'invalid form'
    form =UserForm()

    data = {
        'error': error,
        'form': form,
        'token': request.COOKIES.get('token'),
    }

    return render(request, 'auth/edit.html', data)

def redirectWithCookies(url, cookie_name, cookie_data):
    ret = redirect(url)
    ret.set_cookie(cookie_name,cookie_data, httponly=True)
    return ret
