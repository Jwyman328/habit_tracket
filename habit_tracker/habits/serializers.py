from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Habit, activity, Daily_Habit

from django.contrib.auth.models import User

class regular_Habit_serializer(serializers.ModelSerializer):
    """Serialize only fields of the Habit Model."""

    class Meta:
        model = Habit 
        fields = "__all__"

class Habit_serializer(serializers.ModelSerializer):
    """Serialize Habit Model with additional of creating a Habit."""

    def create(self, validated_data):
        newHabit = Habit.objects.create(**validated_data)
        newHabit.save()
        return newHabit
    
    class Meta:
        model = Habit 
        fields =  "__all__" 


class activity_serializer(serializers.ModelSerializer):
    """Serialize activity models and add data from corresponding Habit model.   

        Keyword Arguments
        -----------------
        title: title of the activity models associated Habit model
        type_of_habit: type_of_habit of the activity models associated Habit model
            either daily or total
        
        Methods
        --------------
        get_title:
            Return title object from associated Habit model.
        get_type_of_habit:
            Return type_of_habit from associated Habit model.
        
    
    """
    title = serializers.SerializerMethodField()
    type_of_habit = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        """Return title object from associated Habit model."""
        title = obj.habit.title
        return title

    def get_type_of_habit(self,obj):
        """Return type_of_habit from associated Habit model."""
        type_of_habit = obj.habit.type_of_habit
        return type_of_habit

    class Meta:
        model = activity
        fields = '__all__'


class sign_up_serializer(serializers.ModelSerializer):
    """Create a new user and return associated jwt token.

    The password and username will be validated only for length.
    
    Keyword Arguments
    -----------------
    password: password takenfrom the users post when signing up
    token: JWT token created for new user

    Methods
    ------------
    get_token:
        Create a unique JWT token for the user to use with thier requests.
    create:
        create a User object if username and password validated.

    """
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        """Create a unique JWT token for the user to use with thier requests."""

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """create a User object if username and password validated."""
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
    """ Serialize Daily_habit models."""
    class Meta:
        model = Daily_Habit
        fields = '__all__'

