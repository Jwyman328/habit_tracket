from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


from .models import Habit, activity, Daily_Habit
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
        Habit.objects.create(start_date="2018-3-28", end_date="2018-3-28",
            type_of_habit='timed', title='test', goal_amount=5, completed=False, user=newUser)

        client = Client()
        client.login(username='testtest', password='password')
        response = client.get(reverse('individual_habit', kwargs={'id': 1}), )
        self.assertEqual(response.status_code, 200)

    def test_habit_post_status_201(self):
        newUser = self.create_user()
        client = Client()
        client.login(username='testtest', password='password')
        
        response = client.post(reverse('create_habit'), data=json.dumps({'start_date':  "2018-3-28", 'end_date':"2018-3-28",
            'type_of_habit':'timed', 'title':'test', 'goal_amount': 5, 'completed':False, 'user': newUser.username},cls= DjangoJSONEncoder),  content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_habit_post_model(self):
        newUser = self.create_user()
        client = Client()
        client.login(username='testtest', password='password')
        
        response = client.post(reverse('create_habit'), data=json.dumps({'start_date':  "2018-3-28", 'end_date':"2018-3-28",
            'type_of_habit':'timed', 'title':'test', 'goal_amount': 5, 'completed':False, 'user': newUser.username},cls= DjangoJSONEncoder),  content_type="application/json")

        newHabit = Habit.objects.get(id=1)
        self.assertEqual(newHabit.start_date, datetime.date(2018,3,28) )
        self.assertEqual(newHabit.end_date, datetime.date(2018,3,28) )
        self.assertEqual(newHabit.type_of_habit, 'timed' )
        self.assertEqual(newHabit.goal_amount, 5 )
        self.assertEqual(newHabit.completed, False )
        self.assertEqual(newHabit.user, newUser )

    def test_get_all_habits_for_date(self):
        newHabit = self.create_habit() # date of habit is datetime.date(2018,3,28), end_date=datetime.date(2018,3,28)
        # need to get any habit that a specific date falls in between 
        client = Client()
        client.login(username='testtest', password='password')

        response = client.get(reverse('all_habits_for_specific_date', kwargs={'year': 2018,'month':3,'day':28}))
        self.assertEqual(response.status_code, 200)

    def test_habit_amount_total_for_date(self):
        self.create_activity()
        client = Client()
        client.login(username='testtest', password='password')

        response = client.get(reverse('habit_total_acumulated_for_specific_date', kwargs={'habit_id':1,'year': 2018,'month':3,'day':28}))
        self.assertEqual(response.status_code, 200)

    def test_habit_completed_turns_to_completed_when_true(self):
        self.create_activity_pass_checked_habit()
        habit = Habit.objects.get(id=1)
        self.assertTrue(habit.completed)


class Test_activity(TestBase):

    def test_activity_get(self):
        newHabit = self.create_habit()
        # subtract times to get total_time 
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        total_time = end_time - start_time 
        newActivity = activity.objects.create(habit=newHabit, start_time=start_time, end_time=end_time, total_time=total_time)

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
        response = client.post(reverse('create_activity'), data=json.dumps({'habit_id':newHabit.id,'start_time': datetime.datetime.now(), 'end_time': datetime.datetime.now()},cls= DjangoJSONEncoder ),
             content_type="application/json")
        self.assertEqual(response.status_code, 201)


    def test_activity_post_model(self):
        newHabit = self.create_habit()
        client = Client()
        client.login(username='testtest', password='password')

        start_time = datetime.datetime(2019, 11, 18, 22, 44, 56, 43000)
        end_time = datetime.datetime(2019, 11, 18, 22, 45, 56, 43000)

        #create a habit 
        response = client.post(reverse('create_activity'), data=json.dumps({'habit_id':newHabit.id,'start_time': start_time , 'end_time':end_time},cls= DjangoJSONEncoder ),
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

    def test_today_habit_activies_query_return(self):
        self.create_activity()
        client = Client()
        client.login(username='testtest', password='password')
        
        date = datetime.date(2018,11,18)
        response = client.get(reverse('individual_habit_date_activity', kwargs={'habit_id': 1, 'year': 2018,'month':3,'day':28}))
        self.assertEqual(response.status_code, 200)

    def test_update_activity_stop_time_put_request(self):
        self.create_activity()
        client = Client()
        client.login(username='testtest', password='password')

        response = client.put(reverse('update_activity_end_time', kwargs={'activity_id':1,'year': 2018,'month':3,'day':28, 'hr':13, 'minute':25,'sec':25}))
        self.assertEqual(response.status_code, 200)

    def test_habit_activity_count_increments(self):
        """when an activity is made, that habit should increment the amount of times it has been done """
        self.create_activity()
        habit = Habit.objects.get(id=1)
        self.assertEqual(habit.current_times_activity_done,1)

    def test_habit_amount_time_accumulated_increments(self):
        """when a timed habit creates an activity the total habit time should be incremented by the"""
        self.create_activity()
        habit = Habit.objects.get(id=1)
        self.assertTrue(habit.current_completed_timed_amount != 0)

        
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


class Test_daily_habit(TestBase):

    def test_daily_habit_create(self):
        self.create_activity()
        daily_habits = Daily_Habit.objects.all()
        self.assertEqual(len(daily_habits), 1)
        
