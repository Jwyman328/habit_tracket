from django.test import TestCase

from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


from habits.models import Habit, activity

import datetime
import json


class TestBase(TestCase):
    def create_user(self):
        newUser = User.objects.create_user(username='testtest', password='password')
        newUser.save()
        return newUser

    def create_habit(self):
        newUser = self.create_user()
        newHabit = Habit.objects.create(start_date=datetime.date(2018,3,28), end_date=datetime.date(2018,3,28),
            type_of_habit='timed', title='test', goal_amount=5, completed=False, user=newUser)

        return newHabit
    
    def create_activity(self):
        newHabit = self.create_habit()
        start_time = datetime.datetime(2019, 11, 18, 22, 44, 56, 43000)
        end_time = datetime.datetime(2019, 11, 18, 22, 45, 56, 43000)

        newActivity = activity.objects.create(habit=newHabit, start_time = start_time, end_time=end_time)
        newActivity.save()