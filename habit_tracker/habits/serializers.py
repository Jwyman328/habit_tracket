from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Habit, activity

from django.contrib.auth.models import User



class Habit_serializer(serializers.ModelSerializer):

    def create(self, validated_data):
        newHabit = Habit.objects.create(**validated_data)
        for obj in validated_data:
            print(obj)
        newHabit.save()
        return newHabit
    
    class Meta:
        model = Habit 
        fields = "__all__"


class activity_serializer(serializers.ModelSerializer):

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

