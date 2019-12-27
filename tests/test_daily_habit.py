from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


from habits.models import Habit, activity, Daily_Habit
from test_tools.test_tools import TestBase

import datetime
import json

class Test_daily_habit(TestBase):

    def test_daily_habit_create(self):
        self.create_activity()
        daily_habits = Daily_Habit.objects.all()
        self.assertEqual(len(daily_habits), 1)

    def test_multiple_daily_habits_created(self):
       
        newUser = self.create_user()
        newHabit = Habit.objects.create(start_date="2018-3-28", end_date="2018-3-30",
            type_of_habit='timed', title='test', goal_amount=5, completed=False, user=newUser)
        newHabit.save()

        daily_habits = Daily_Habit.objects.all()
        self.assertEqual(len(daily_habits), 3)

    def test_daily_habit_goal_checked_completed(self):
        newHabit = self.create_daily_checked_habit()

        start_time = datetime.datetime(2018, 3, 28, 22, 44, 56, 43000)
        end_time = datetime.datetime(2018, 3, 28, 22, 45, 56, 43000)
        total_time = end_time - start_time
        newActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time, total_time=total_time)
        secondActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time, total_time=total_time)

        newActivity.save()
        secondActivity.save()

        daily_habit = Daily_Habit.objects.get(id=1)
        self.assertTrue(daily_habit.completed)

    def test_get_daily_habit_data_by_id(self):
        newHabit = self.create_daily_checked_habit()

        start_time = datetime.datetime(2018, 3, 28, 22, 44, 56, 43000)
        end_time = datetime.datetime(2018, 3, 28, 22, 45, 56, 43000)
        total_time = end_time - start_time
        newActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time, total_time=total_time)
        secondActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time, total_time=total_time)
        newActivity.save()
        secondActivity.save()

        client = Client()
        client.login(username='testtest', password='password')

        response = client.get(reverse('specific_daily_habit_data', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_get_multiple_daily_habits_by_dates(self):
        newHabit = self.create_daily_checked_habit()

        start_time = datetime.datetime(2018, 3, 28, 22, 44, 56, 43000)
        end_time = datetime.datetime(2018, 3, 28, 22, 45, 56, 43000)
        total_time = end_time - start_time
        newActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time, total_time=total_time)
        secondActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time, total_time=total_time)
        newActivity.save()
        secondActivity.save()

        client = Client()
        client.login(username='testtest', password='password')

        response = client.get(reverse('daily_habits_by_date', kwargs={'year':'2019','month':'3','day':'28'}))
        self.assertEqual(response.status_code, 200)
