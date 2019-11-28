from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Habit, activity, Daily_Habit

from django.contrib.auth.models import User

class regular_Habit_serializer(serializers.ModelSerializer):
    class Meta:
        model = Habit 
        fields = "__all__"

class Habit_serializer(serializers.ModelSerializer):


    def create(self, validated_data):
        newHabit = Habit.objects.create(**validated_data)
        for obj in validated_data:
            print(obj)
        newHabit.save()
        return newHabit
    
    class Meta:
        model = Habit 
        fields =  "__all__" #('daily_timed_goal_completed_dict','daily_checked_goal_completed_dict' )


class activity_serializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    type_of_habit = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        title = obj.habit.title
        return title

    def get_type_of_habit(self,obj):
        type_of_habit = obj.habit.type_of_habit
        return type_of_habit

    class Meta:
        model = activity
        fields = '__all__'


class sign_up_serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        if len(username) > 5 and len(password) > 5:
            newUser = User.objects.create_user(**validated_data) # username=username,password=password
            return newUser
        else:
            return 'error' # not a valid error will need changing 

    class Meta:
        model = User
        fields = ('token','username', 'password' )

class Daily_habit_serializer(serializers.ModelSerializer):

    class Meta:
        model = Daily_Habit
        fields = '__all__'

