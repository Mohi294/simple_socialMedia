import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from user.serializers import ( SimpleUserSerializer,UserSerializer)


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {'username': 'testcase', 'email': 'test@localhost.app',
                'password': 'some_strong_psw', 'password2': 'some_strong_psw',
                'first_name': 'first_test', 'last_name': 'last_test'}
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('token_obtain_pair')
        self.register_url = reverse('user_register')
        user_data = {'username': 'testcase', 'email': 'test@localhost.app',
                    'password': 'some_strong_psw', 'password2': 'some_strong_psw',
                    'first_name': 'first_test', 'last_name': 'last_test'}
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
    
    def test_login(self):
        data = {'username': 'testcase', 'email': 'test@localhost.app',
                'password': 'some_strong_psw', 'password2': 'some_strong_psw',
                'first_name': 'first_test', 'last_name': 'last_test'}

        response = self.client.post(
            self.register_url, data, format='json'
        )
        
        username = response.data['username']
        user = User.objects.get(username=username)
        
        user.save()
        
        res = self.client.post(self.login_url, data, format='json')
        self.assertEqual(res.status_code, 200)
