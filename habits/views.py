#django imports
from django.shortcuts import render
from django.utils import timezone

#local imports
from .models import Habit, activity, Daily_Habit
from .serializers import Habit_serializer, activity_serializer, sign_up_serializer, regular_Habit_serializer, Daily_habit_serializer

# 3rd party package imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

#python imports
import pytz
from pytz import timezone
import datetime
import json


class individual_habit_view(APIView):
    """Return Individual Habit Data."""

    def get(self, request, id):
        habit_id = id
        my_query = Habit.objects.get(id=habit_id)
        serialized_data = Habit_serializer(my_query)
        return Response(serialized_data.data, status.HTTP_200_OK )

class create_habit(APIView):
    """Create a Habit model."""

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
    """Return individual activity data."""

    def get(self, request, id):
        activity_id = id
        activity_query = activity.objects.get(id=activity_id)
        serialized_data = activity_serializer(activity_query)
        return Response(serialized_data.data, status.HTTP_200_OK)

class all_completed_activities_for_date(APIView):
    """Return all completed activities for specific date."""

    def get(self, request, year, month, day):
        activity_date = datetime.date(year,month,day)
        sctivity_date_over = activity_date + datetime.timedelta(days=1)
        user = request.user
        all_activities_for_date = activity.objects.filter(habit__user=user).filter(start_time__gte = activity_date).filter(total_time__gt = datetime.timedelta(0,0,0))
        all_activities_for_habit  = all_activities_for_date.filter(start_time__lt = sctivity_date_over)
        # sort them by start time 
        all_activities_for_habit = all_activities_for_habit.order_by('-start_time')
        serialized_data = activity_serializer(all_activities_for_habit , many=True)
        return Response(serialized_data.data, status.HTTP_200_OK)

class timed_activities_for_date(APIView):
    """Return activities with a timed habit type_of_habit for specific date."""

    def get(self, request, year, month, day):
        activity_date = datetime.date(year,month,day)
        sctivity_date_over = datetime.date(year,month,day + 1)
        user = request.user
        all_activities_for_date = activity.objects.filter(habit__user=user).filter(habit__type_of_habit='timed').filter(start_time__gte = activity_date)
        all_activities_for_habit  = all_activities_for_date.filter(start_time__lt = sctivity_date_over)
        # sort them by start time 
        all_activities_for_habit = all_activities_for_habit.order_by('-start_time')
        serialized_data = activity_serializer(all_activities_for_habit , many=True)
        return Response(serialized_data.data, status.HTTP_200_OK)

class checked_activities_for_date(APIView):
    """Return activities with a checked habit type_of_habit for specific date."""

    def get(self, request, year, month, day):
        activity_date = datetime.date(year,month,day)
        sctivity_date_over = datetime.date(year,month,day + 1)
        user = request.user
        all_activities_for_date = activity.objects.filter(habit__user=user).filter(habit__type_of_habit='checked').filter(start_time__gte = activity_date)
        all_activities_for_habit  = all_activities_for_date.filter(start_time__lt = sctivity_date_over)
        # sort them by start time 
        all_activities_for_habit = all_activities_for_habit.order_by('-start_time')
        serialized_data = activity_serializer(all_activities_for_habit , many=True)
        return Response(serialized_data.data, status.HTTP_200_OK)

class create_activity(APIView):
    """Create an activity."""

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
    """Return all activities for a specific Habit."""

    def get(self,request, id):
        habit_id = id
        this_habit = Habit.objects.get(id=habit_id)
        all_activities_for_habit = activity.objects.filter(habit=this_habit)
        serialized_activities = activity_serializer(all_activities_for_habit, many=True)
        return Response(serialized_activities.data, status.HTTP_200_OK)

class individual_habit_date_activity_view(APIView):
    """Return all activities for specified habit of a specified date"""

    def get(self,request, habit_id, year, month, day):
        ## make a datetime date with year month day 
        date_wanted = datetime.datetime(year,month,day)
        ## get all activities for this habit that are on this day
        ## so not less than this day, or greaterthan or equal to a day after 
        dayIncrement = datetime.timedelta(days=1)
        date_past = date_wanted + dayIncrement
        this_habit = Habit.objects.get(id=habit_id)
        all_activities_for_habit = activity.objects.filter(habit=this_habit).filter(start_time__gte = date_wanted)
        all_activities_for_habit  = all_activities_for_habit.filter(start_time__lt = date_past)

        serialized_activities = activity_serializer(all_activities_for_habit, many=True)
        return Response(serialized_activities.data, status.HTTP_200_OK)

class all_habits_for_specific_date(APIView):
    """Return all habits that contain a specified date in their date range."""

    def get(self,request,year,month,day):
        # query just the users habits, then based off of date 
        # create a date 
        date_wanted = datetime.datetime(year,month,day)
        userHabits = Habit.objects.filter(user=request.user).filter(start_date__lte=date_wanted).filter(end_date__gte = date_wanted)
        serialized_data = regular_Habit_serializer(userHabits, many=True)
        return Response(serialized_data.data, status.HTTP_200_OK )

class habit_total_acumulated_for_specific_date(APIView):
    """Return data of a habit's accumulated time and accumulated count for a date."""

    def get(self, request, habit_id, year, month, day):
        # get habit, then query activities for this date 
        ## make a datetime date with year month day 
        date_wanted = datetime.datetime(year,month,day)
        ## get all activities for this habit that are on this day
        dayIncrement = datetime.timedelta(days=1)
        date_past = date_wanted + dayIncrement
        this_habit = Habit.objects.get(id=habit_id)
        ## not less than this day, or greaterthan or equal to a day after 
        all_activities_for_habit = activity.objects.filter(habit=this_habit).filter(start_time__gte = date_wanted)
        all_activities_for_habit  = all_activities_for_habit.filter(start_time__lt = date_past)
        ## now add up the total accumulated time and accumulated count 

        accumulated_data = {'accumulated_time':datetime.timedelta(0), 'accumulated_count':0}
        for activity_of_date in all_activities_for_habit:
            if activity_of_date.total_time:
                accumulated_data['accumulated_time'] += activity_of_date.total_time
            else:
                pass
            accumulated_data['accumulated_count'] += 1  
        #no serializer for this data, manually convert it to json 
        # turn delta time to string, json wont accept delta datetime
        accumulated_data['accumulated_time'] = str(accumulated_data['accumulated_time'] )
        jsonString = json.dumps(accumulated_data)
        jsonData = json.loads( jsonString)
        return Response(jsonData, status.HTTP_200_OK )


class update_activity_end_time(APIView):
    """Update activity end time when timed activity is stopped."""

    def put(self,request,activity_id, year,month,day,hr,minute,sec):

        eastern = timezone('US/Eastern')
        end_time = datetime.datetime(year,month,day,hr,minute,sec)
        end_time = eastern.localize(end_time)
        this_activity = activity.objects.get(id=activity_id)
        this_activity.end_time = end_time

        #also set the total time as the differnece of the start time and end time 
        total_time = end_time  - this_activity.start_time 
        this_activity.total_time = total_time
        this_activity.save()
        return Response('activity updated', status.HTTP_200_OK )

        
class sign_up_user(APIView):
    """Create a new user with passed username and password."""

    # allow anyone to access the ability to make a user
    permission_classes = [AllowAny]

    def post(self,request):
        username_password = request.data 
        serialized_data = sign_up_serializer(data = username_password)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class specific_daily_habit_data(APIView):
    """Return specific daily_habit data."""

    def get(self,request, id):
        query = Daily_Habit.objects.get(id=id)
        serialized_data = Daily_habit_serializer(query)
        return Response(serialized_data.data, status.HTTP_200_OK )

class daily_habits_by_date(APIView):
    """Return all daily_habits for specified date."""

    def get(self,request, year,month, day):
        habit_day = datetime.date(year,month,day)
        query = Daily_Habit.objects.filter(date=habit_day)
        serialized_data = Daily_habit_serializer(query, many=True)
        return Response(serialized_data.data, status.HTTP_200_OK )





