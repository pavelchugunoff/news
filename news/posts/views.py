import json
from django.shortcuts import redirect, render
import requests
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
import time
from authentication.serializers import UserSerializer
from authentication.models import User
from .models import Post
from .forms import PostForm
from .utils.slugify import slugify
from .serializers import PostSerializer
from authentication.views import redirectWithCookies



class CreatePostAPIView(APIView):
    """
    API class for create the post
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        post = request.data
        user = request.user

        post['author'] = user.username
        post['article'] = user.id + int(time.time())
        post['title_url'] = slugify(post['title'])
        post['views'] = 0
        post['rate'] = 0

        serializer = PostSerializer(data=post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    API class for editing and showing a post
    """  
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(Post.objects.get(article=request.data['article']))

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get("post", {})
        serializer = PostSerializer(Post.objects.get(article=request.data.get('article')), data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(serializer.data, status=status.HTTP_200_OK)


class RatePostAPIView(APIView):
    """
    API post evaluation class.
    Changes the overall rating of the post and if there is no information about it in the user
    creates an array with data about the post
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, title_url):
        post = Post.objects.get(title_url = title_url)
        serializer_data = PostSerializer(post).data
        rate = request.data['rate']
        
        if str(post.article) not in json.loads(request.user.posts_info):
            post_info = {
                "rate":0,
                "favorite":False
            }
        else:
            post_info = json.loads(request.user.posts_info)[str(post.article)]
        
        user_rate = post_info['rate']

        if user_rate != 0:
            serializer_data['rate'] = str( int(serializer_data['rate']) - int(user_rate))
        
        if rate == 0:
             serializer_data['rate'] = str( int(serializer_data['rate']) - int(user_rate))
        
        
        serializer_data['rate'] = str(int(serializer_data['rate']) + int(rate))
        
        serializer = PostSerializer(post, data=serializer_data, partial=True)         
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = UserSerializer(request.user).data
        posts_info = json.loads(user_data['posts_info'])
        post_info['rate'] = rate
        posts_info[str(post.article)] = post_info
        user_data['posts_info'] = json.dumps(posts_info)
        user_serializer = UserSerializer(request.user, user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoritePostAPIView(APIView):
    """
    API class for adding a post to favorites. 
    Adds a post to favorites and if there is no information about 
    it in the user creates an array with data about the post
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, title_url):
        post = Post.objects.get(title_url = title_url)
        fav = True
        
        if str(post.article) not in json.loads(request.user.posts_info):
            post_info = {
                "rate":0,
                "favorite":False
            }
        else:
            post_info = json.loads(request.user.posts_info)[str(post.article)]
            if post_info['favorite'] == True: fav = False
        
        
        user_data = UserSerializer(request.user).data
        posts_info = json.loads(user_data['posts_info'])
        post_info['favorite'] = fav
        posts_info[str(post.article)] = post_info
        user_data['posts_info'] = json.dumps(posts_info)
        user_serializer = UserSerializer(request.user, user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        
        return Response(post_info, status=status.HTTP_200_OK)


class GetPostsAPIView(APIView):
    """
    API class for sorting all posts. Returns a list of posts with the sorting that the user specified
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        sort=request.data.get('sort')
        posts = Post.objects.all()
        
        if sort == 'date':
            posts = list(sorted(posts, key = lambda x: x.date_created, reverse=True))
        elif sort == 'rate':
            posts = list(reversed(posts.order_by('rate')))
        elif sort == 'views':
            posts = list(reversed(posts.order_by('views')))
        else:
            return Response({'details':'Error with sort'}, status=status.HTTP_400_BAD_REQUEST)

        temp = posts
        posts = {}
        i = 1
        for post in temp:
            posts['post_'+str(i)] = PostSerializer(post).data
            i+=1

        return Response(posts, status=status.HTTP_200_OK)


class RemovePostAPIView(APIView):
    """
    API class that deletes the post
    """
    def post(self, request, title_url):
        post = Post.objects.get(title_url=title_url)
        post.delete()
        return Response({"details":"Post deleted sucessfully!"}, status=status.HTTP_200_OK)


def EditPostView(request, title_url):

    if request.COOKIES.get("token") == None:
        if requests.get('https://0.0.0.0:8000/auth/api/update/',headers={'Authorization':'Bearer '+request.COOKIES.get('token')}).status_code != 200:
            return redirect('http://0.0.0.0:8000/')
        return redirect('http://0.0.0.0:8000/')

    error = ''

    post = Post.objects.get(title_url=title_url)

    serializer_data = PostSerializer(post).data

    if request.method == 'POST':
        form = PostForm(request.POST)
        serializer_data['title'] = form.data.get('title')
        serializer_data['title_url'] = slugify(form.data.get('title'))
        serializer_data['content'] = form.data.get('content')
        serializer_data['summary'] = form.data.get('summary')

        update_req = requests.put('http://0.0.0.0:8000/post/api/update/', data = serializer_data,
         headers={'content-type':'application/json', 'Authorization':'Bearer ' + request.COOKIES.get('token')})

        if update_req.status_code == 200:
            redirectWithCookies('http://0.0.0.0:8000/post/'+serializer_data['title_url'],'token',request.COOKIES.get('token'))
        else:
            error = 'invalid form'
    form = PostForm()

    data = {
        'error': error,
        'form': form,
        'title_url':title_url
    }

    return render(request, 'posts/edit.html', data)

def FeedView(request):
    sort = 'views'
    count = 5
    
    if request.method == 'POST':
        sort = request.POST.get('sort')
        count = int(request.POST.get('count'))

    body = {
        "sort":sort
    }

    headers={
        'Content-Type':'application/json'
    }

    posts_req = requests.post('http://0.0.0.0:8000/post/api/getposts/', data = json.dumps(body), headers = headers)


    posts = list(json.loads(posts_req.text).values())

    p = Paginator(posts,count)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number == '1'
    page_obj = p.get_page(page_number)
    page_next = page_number
    page_prev = page_number
    if page_obj.has_next():
        page_next = page_obj.next_page_number()
    if page_obj.has_previous():
        page_prev = page_obj.previous_page_number()
    
       
    return render(request, 'posts/posts.html', {'page_obj':page_obj,'previous':page_prev,'next':page_next})


def CreatePostView(request):
    
    if request.COOKIES.get("token") == None:
        if requests.get('https://0.0.0.0:8000/auth/api/update/',headers={'Authorization':'Bearer '+request.COOKIES.get('token')}).status_code != 200:
            return redirect('http://0.0.0.0:8000/')
        return redirect('http://0.0.0.0:8000/')
    
    error = ''

    if request.method == 'POST':
        form = PostForm(request.POST)
        
        title = form.data.get('title')
        content = form.data.get('content')
        summary = form.data.get('summary')
        

        body = {
            "title":title,
            "content":content,
            "summary":summary,
        }
        headers = {'content-type': 'application/json', 'Authorization':'Bearer '+ request.COOKIES.get('token')}

        body = json.dumps(body)
        create_req = requests.post('http://0.0.0.0:8000/post/api/create/',data=body,headers=headers)
        
        if create_req.status_code == 201:
            return redirectWithCookies('http://0.0.0.0:8000/post/'+str(json.loads(create_req.text)['title_url']),"token", request.COOKIES.get('token'))
        else:
            error = 'invalid form'

    form = PostForm()

    data = {
        'error': error,
        'form': form,
    }

    return render(request, 'posts/create.html', data)

def PostView(request, title_url):

    

    if request.method == 'POST':
        if request.POST['action_rate'] != None: 
            rate_req = requests.post('http://0.0.0.0:8000/post/api/'+title_url+'/rate/',headers={'content-type':'application/json',
            'Authorization':'Bearer '+request.COOKIES.get('token')}, data=json.dumps({'rate':request.POST['action_rate']}))


    else:
        serializer_data = PostSerializer(Post.objects.get(title_url = title_url)).data
        serializer_data['views'] = str(int(serializer_data['views']) + 1)
        serializer = PostSerializer(Post.objects.get(title_url = title_url), serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    serializer_data = PostSerializer(Post.objects.get(title_url = title_url)).data


    post = Post.objects.get(title_url = title_url)
    serializer_data['token'] = request.COOKIES.get('token')


    return render(request, 'posts/post.html', serializer_data)


 
