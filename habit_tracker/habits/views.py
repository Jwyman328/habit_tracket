from django.shortcuts import render

from .models import Habit, activity
from .serializers import Habit_serializer, activity_serializer, sign_up_serializer

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

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
        print(id_num)
       
        habit_object = Habit.objects.get(id = id_num) 
        del data['habit_id']
        data['habit'] = habit_object
        print(data)
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





