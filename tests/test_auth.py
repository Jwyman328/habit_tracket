from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


from habits.models import Habit, activity, Daily_Habit
from test_tools.test_tools import TestBase

import datetime
import json

class Auth_test(TestBase):

    def test_sign_in_status(self):
        # post to the sign in page and get a good response 
        self.create_user()
        usernamePassword = {'username':'testtest', 'password':'password'}

        client = Client()
        response = client.post(reverse('login'), json.dumps(usernamePassword), content_type='application/json')   
        self.assertEqual(response.status_code, 200)

    def test_sign_up_status(self):
        usernamePassword = {'username':'testtest', 'password':'password'}

        client = Client()
        response = client.post(reverse('sign_up'), json.dumps(usernamePassword), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_sign_up_user_created(self):
        usernamePassword = {'username':'testtest', 'password':'password'}

        client = Client()
        response = client.post(reverse('sign_up'), json.dumps(usernamePassword), content_type='application/json')
        
        new_user_query_set = User.objects.all()
        self.assertEqual(len( new_user_query_set), 1)
        self.assertEqual(new_user_query_set[0].username, 'testtest')