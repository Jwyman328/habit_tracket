from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


from habits.models import Habit, activity, Daily_Habit
from test_tools.test_tools import TestBase

import datetime
import json



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