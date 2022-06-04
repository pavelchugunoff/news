import json
from django.shortcuts import redirect, render
import requests

from authentication.forms import UserForm
from authentication.models import User
from authentication.serializers import UserSerializer
from posts.serializers import PostSerializer
from posts.models import Post
# Create your views here.

def UserProfileView(request):
    if request.COOKIES.get("token") == None:
        if requests.get('https://0.0.0.0:8000/auth/api/update/',headers={'Authorization':'Bearer '+request.COOKIES.get('token')}).status_code != 200:
            return redirect('http://0.0.0.0:8000/')
        return redirect('http://0.0.0.0:8000/')
    
    username = json.loads(requests.get('http://0.0.0.0:8000/auth/api/update',headers={'content-type':'application/json','Authorization':'Bearer '+request.COOKIES.get('token')}).text)['username']
    posts = Post.objects.all()
    created_posts = {}
    i=0
    for post in posts:
        if post.author == username:
            created_posts[str(i)] = PostSerializer(post).data
            i += 1

    posts = json.loads(UserSerializer(User.objects.get(username = username)).data.get('posts_info'))
    favorite_posts = {}
    i=0
    for key,post in posts.items():
        try:
            if post['favorite'] == True:
                favorite_posts[str(i)] = PostSerializer(Post.objects.get(article=key)).data
                i += 1
        except Post.DoesNotExist:
            pass

    created_posts = list(created_posts.values())
    favorite_posts = list(favorite_posts.values())
            

    return render(request, 'user/profile.html',{'user':UserSerializer(User.objects.get(username=username)).data,'created':created_posts,'favorite':favorite_posts})

    