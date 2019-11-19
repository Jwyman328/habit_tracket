from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


from .models import Habit, activity
from test_tools.test_tools import TestBase

import datetime
import json



# Create your tests here.
# use rest framework to give the ability to make habits or activities 
## split up into habit vs. activities 
class habit_test(TestBase):

    def test_habit_get_status(self):
        # first create a user obj before you create a  habit obj before you request data for it 
        newUser = self.create_user()
        Habit.objects.create(start_date=datetime.date(2018,3,28), end_date=datetime.date(2018,3,28),
            type_of_habit='timed', title='test', goal_amount=5, completed=False, user=newUser)

        client = Client()
        client.login(username='testtest', password='password')
        response = client.get(reverse('individual_habit', kwargs={'id': 1}), )
        self.assertEqual(response.status_code, 200)

    def test_habit_post_status_201(self):
        newUser = self.create_user()
        client = Client()
        client.login(username='testtest', password='password')
        
        response = client.post(reverse('create_habit'), data=json.dumps({'start_date':  datetime.date(2018,3,28), 'end_date':datetime.date(2018,3,28),
            'type_of_habit':'timed', 'title':'test', 'goal_amount': 5, 'completed':False, 'user': newUser.username},cls= DjangoJSONEncoder),  content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_habit_post_model(self):
        newUser = self.create_user()
        client = Client()
        client.login(username='testtest', password='password')
        
        response = client.post(reverse('create_habit'), data=json.dumps({'start_date':  datetime.date(2018,3,28), 'end_date':datetime.date(2018,3,28),
            'type_of_habit':'timed', 'title':'test', 'goal_amount': 5, 'completed':False, 'user': newUser.username},cls= DjangoJSONEncoder),  content_type="application/json")

        newHabit = Habit.objects.get(id=1)
        self.assertEqual(newHabit.start_date, datetime.date(2018,3,28) )
        self.assertEqual(newHabit.end_date, datetime.date(2018,3,28) )
        self.assertEqual(newHabit.type_of_habit, 'timed' )
        self.assertEqual(newHabit.goal_amount, 5 )
        self.assertEqual(newHabit.completed, False )
        self.assertEqual(newHabit.user, newUser )


class Test_activity(TestBase):

    def test_activity_get(self):
        newHabit = self.create_habit()
        newActivity = activity.objects.create(habit=newHabit, start_time=datetime.datetime.now(), end_time=datetime.datetime.now(), total_time=0)

        client = Client()
        client.login(username='testtest', password='password')
        response = client.get(reverse('individual_activity', kwargs={'id':1}))
        self.assertEqual(response.status_code, 200)



    def test_activity_post(self):
        # create user and login
        newHabit = self.create_habit()
        client = Client()
        client.login(username='testtest', password='password')

        #create a habit 
        response = client.post(reverse('create_activity'), data=json.dumps({'habit_id':newHabit.id,'start_time': datetime.datetime.now(), 'end_time': datetime.datetime.now(), 'total_time':0},cls= DjangoJSONEncoder ),
             content_type="application/json")
        self.assertEqual(response.status_code, 201)


    def test_activity_post_model(self):
        newHabit = self.create_habit()
        client = Client()
        client.login(username='testtest', password='password')

        start_time = datetime.datetime(2019, 11, 18, 22, 44, 56, 43000)
        end_time = datetime.datetime(2019, 11, 18, 22, 45, 56, 43000)

        #create a habit 
        response = client.post(reverse('create_activity'), data=json.dumps({'habit_id':newHabit.id,'start_time': start_time , 'end_time':end_time, 'total_time':0},cls= DjangoJSONEncoder ),
             content_type="application/json")

        newActivity = activity.objects.get(id=1)
        self.assertEqual(newActivity.habit, newHabit)
        self.assertEqual(newActivity.start_time.time(), start_time.time())
        self.assertEqual(newActivity.end_time.time(), end_time.time() )
    
    
    def test_habit_activity_list_get_status_200(self):
        self.create_activity()
        client = Client()
        client.login(username='testtest', password='password')

        response = client.get(reverse('individual_habit_activity_list', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        
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


