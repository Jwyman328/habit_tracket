from django.shortcuts import render

from .models import Habit, activity
from .serializers import Habit_serializer, activity_serializer, sign_up_serializer, regular_Habit_serializer

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from django.utils import timezone
import pytz
from pytz import timezone

import datetime

class individual_habit_view(APIView):

    def get(self, request, id):
        habit_id = id
        my_query = Habit.objects.get(id=habit_id)
        serialized_data = Habit_serializer(my_query)
        return Response(serialized_data.data, status.HTTP_200_OK )

class create_habit(APIView):

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user
        data['completed'] = False
        newHabit = Habit.objects.create(**data)
        newHabit.save()

        if newHabit:
            return Response( 'habit created', status.HTTP_201_CREATED) 
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)

class individual_activity(APIView):

    def get(self, request, id):
        activity_id = id
        activity_query = activity.objects.get(id=activity_id)
        serialized_data = activity_serializer(activity_query)
        return Response(serialized_data.data, status.HTTP_200_OK)

class create_activity(APIView):

    def post(self, request):
        # current format of data sent = {'habit_id':newHabit.id,'start_time': datetime.datetime.now(), 'end_time': datetime.datetime.now(), 'total_time':0}
        data = request.data 
        id_num = data['habit_id']       
        habit_object = Habit.objects.get(id = id_num) 
        del data['habit_id']
        data['habit'] = habit_object
       
        eastern = timezone('US/Eastern')
        newDate = datetime.datetime.now()
        newDate = eastern.localize(newDate)
        data['start_time'] = newDate
        newActivity = activity.objects.create(**data)
        newActivity.save()
        if (newActivity):
            return Response('activity created', status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)

class individual_habit_activity_list(APIView):

    def get(self,request, id):
        habit_id = id
        this_habit = Habit.objects.get(id=habit_id)
        all_activities_for_habit = activity.objects.filter(habit=this_habit)
        serialized_activities = activity_serializer(all_activities_for_habit, many=True)
        return Response(serialized_activities.data, status.HTTP_200_OK)

class individual_habit_date_activity_view(APIView):
    """return all activities for specified habit of specified date """
    def get(self,request, habit_id, year, month, day):
        ## make a datetime date with year month day 
        date_wanted = datetime.datetime(year,month,day)
        ## get all activities for this habit that are on this day
        ## so not less than this day, or greaterthan or equal to a day after 
        date_past = datetime.datetime(year,month,day + 1) 
        this_habit = Habit.objects.get(id=habit_id)
        all_activities_for_habit = activity.objects.filter(habit=this_habit).filter(start_time__gte = date_wanted)
        all_activities_for_habit  = all_activities_for_habit.filter(start_time__lt = date_past)

        serialized_activities = activity_serializer(all_activities_for_habit, many=True)
        return Response(serialized_activities.data, status.HTTP_200_OK)

class all_habits_for_specific_date(APIView):

    def get(self,request,year,month,day):
        # query just the users habits, then based off of date 
        # create a date 
        date_wanted = datetime.datetime(year,month,day)
        userHabits = Habit.objects.filter(user=request.user).filter(start_date__lte=date_wanted).filter(end_date__gte = date_wanted)
        serialized_data = regular_Habit_serializer(userHabits, many=True)
        return Response(serialized_data.data, status.HTTP_200_OK )

class update_activity_end_time(APIView):

    def put(self,request,activity_id, year,month,day,hr,minute,sec):

        eastern = timezone('US/Eastern')
        end_time = datetime.datetime(year,month,day,hr,minute,sec)

        end_time = eastern.localize(end_time)
        this_activity = activity.objects.get(id=activity_id)
        this_activity.end_time = end_time

        #also set the total time as the differnece of the start time and end time 
        total_time = end_time  - this_activity.start_time 
        print( total_time)
        this_activity.total_time = total_time
        this_activity.save()
        return Response('activity updated',status.HTTP_200_OK )

        
class sign_up_user(APIView):

    # return the serialized data
    # the view has allowAny ?
    # only accept posts 
    # validate the data 
    # make a token and return it 

    permission_classes = [AllowAny]

    def post(self,request):
        username_password = request.data 
        serialized_data = sign_up_serializer(data = username_password)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)





