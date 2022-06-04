from rest_framework.test import APITestCase
from rest_framework import status
from authentication.serializers import UserSerializer
from authentication.models import User



class RegisterUserAPITestCase(APITestCase):
    url = 'http://0.0.0.0:8000/auth/api/create/'
    def test_post(self):
        data = {'username':'testuser','email':'testemail@test.com','password':'password'}
        response = self.client.post(self.url,data,'json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(True, User.objects.filter(id=response.data['id']).exists())

class UpdateUserAPITestCase(APITestCase):
    url = 'http://0.0.0.0:8000/auth/api/update/'
    def test_get(self):
        create_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_req.data['username'],'password':'password'},'json')
        response = self.client.get(self.url, None, **{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, UserSerializer(User.objects.get(id=create_req.data['id'])).data)
    def test_put(self):
        create_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_req.data['username'],'password':'password'},'json')
        serializer_data = UserSerializer(User.objects.get(id=create_req.data['id'])).data
        serializer_data['username'] = 'johndoe'
        response = self.client.put(self.url,{'user':serializer_data}, **{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']}, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, UserSerializer(User.objects.get(id=create_req.data['id'])).data)

class RemoveUserAPITestCase(APITestCase):
    url = 'http://0.0.0.0:8000/auth/api/delete/'
    def test_post(self):
        create_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        token_req = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_req.data['username'],'password':'password'},'json')
        self.client.post(self.url, None, **{'HTTP_AUTHORIZATION':'Bearer ' + token_req.data['token']})
        self.assertEqual(False, User.objects.filter(id=create_req.data['id']).exists())

class AuthenticateUserAPITestCase(APITestCase):
    url = 'http://0.0.0.0:8000/auth/api/signin/'
    def test_get(self):
        create_req = self.client.post('http://0.0.0.0:8000/auth/api/create/',{'username':'testuser','email':'testemail@test.com','password':'password'},'json')
        response = self.client.post('http://0.0.0.0:8000/auth/api/signin/',{'username':create_req.data['username'],'password':'password'},'json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        check_req = self.client.get('http://0.0.0.0:8000/auth/api/update/', None, **{'HTTP_AUTHORIZATION':'Bearer ' + response.data['token']})
        self.assertEqual(create_req.data,check_req.data)
        
        
        