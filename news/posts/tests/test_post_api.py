import time
from rest_framework.test import APITestCase
from rest_framework import status
from posts.serializers import PostSerializer
from posts.models import Post

class CreatePostAPITestCase(APITestCase):
    url = 'http://0.0.0.0:8000/post/api/create/'
    def test_post(self):
        create_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_req.data['username'],'password':'password'},'json')
        data = {'title':'test','summary':'test post','content':'This is the test post'}
        response = self.client.post(self.url,data,**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(True, Post.objects.filter(article=response.data['article']).exists())

class UpdatePostAPITestCase(APITestCase):
    url = 'http://0.0.0.0:8000/post/api/update/'
    def test_post(self):
        create_user_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_user_req.data['username'],'password':'password'},'json')
        create_post_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test','summary':'test post','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        
        response = self.client.post(self.url,{'article':create_post_req.data['article']},format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostSerializer(Post.objects.get(article=create_post_req.data['article'])).data,response.data)
    def test_put(self):
        create_user_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_user_req.data['username'],'password':'password'},'json')
        create_post_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test','summary':'test post','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        serializer_data = PostSerializer(Post.objects.get(article = create_post_req.data['article'])).data
        serializer_data['title'] = 'test(after put())'
        response = self.client.put(self.url,{'post':serializer_data,'article':serializer_data['article']}, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, PostSerializer(Post.objects.get(article = create_post_req.data['article'])).data)

class RatePostAPITestCase(APITestCase):
    def test_post(self):
        create_user_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_user_req.data['username'],'password':'password'},'json')
        create_post_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test','summary':'test post','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        url='http://0.0.0.0:8000/post/api/'+create_post_req.data['title_url']+'/rate/'
        response = self.client.post(url,{'rate':1},format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostSerializer(Post.objects.get(article = create_post_req.data['article'])).data['rate'],response.data['rate'])
        response = self.client.post(url,{'rate':0},format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostSerializer(Post.objects.get(article = create_post_req.data['article'])).data['rate'],response.data['rate'])
        response = self.client.post(url,{'rate':-1},format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostSerializer(Post.objects.get(article = create_post_req.data['article'])).data['rate'],response.data['rate'])

class FavoritePostAPITestCase(APITestCase):
    def test_post(self):
        create_user_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_user_req.data['username'],'password':'password'},'json')
        create_post_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test','summary':'test post','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        url='http://0.0.0.0:8000/post/api/'+create_post_req.data['title_url']+'/favorite/'
        response = self.client.post(url,format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(True,response.data['favorite'])
        response = self.client.post(url,format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(False,response.data['favorite'])

class RemovePostAPITestCase(APITestCase):
    def test_post(self):
        create_user_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_user_req.data['username'],'password':'password'},'json')
        create_post_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test','summary':'test post','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        url='http://0.0.0.0:8000/post/api/'+create_post_req.data['title_url']+'/delete/'
        self.client.post(url)
        self.assertEqual(False, Post.objects.filter(article=create_post_req.data['article']).exists())

class GetPostsAPITestCase(APITestCase):
    url='http://0.0.0.0:8000/post/api/getposts/'
    def test_post(self):
        create_user_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_user_req.data['username'],'password':'password'},'json')
        create_post1_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test','summary':'test post','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        time.sleep(1)
        create_post2_req= self.client.post('http://0.0.0.0:8000/post/api/create/',{'title':'test2','summary':'test post2','content':'This is the test post'},**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']},format='json')
        self.client.post('http://0.0.0.0:8000/post/api/'+create_post1_req.data['title_url']+'/rate/',{'rate':1},format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.client.post('http://0.0.0.0:8000/post/api/'+create_post2_req.data['title_url']+'/rate/',{'rate':-1},format='json',**{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        serializer_data = PostSerializer(Post.objects.get(title_url = create_post1_req.data['title_url'])).data
        serializer_data['views'] = str(int(serializer_data['views']) + 1)
        serializer = PostSerializer(Post.objects.get(title_url = create_post1_req.data['title_url']), serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = self.client.post(self.url,{'sort':'date'})
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        post = list(response.data.values())[0]
        self.assertEqual(create_post2_req.data['article'],post['article'])
        response = self.client.post(self.url,{'sort':'rate'})
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        post = list(response.data.values())[0]
        self.assertEqual(create_post1_req.data['article'],post['article'])
        response = self.client.post(self.url,{'sort':'views'})
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        post = list(response.data.values())[0]
        self.assertEqual(create_post1_req.data['article'],post['article'])
