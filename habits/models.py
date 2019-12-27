from django.db import models

from django.contrib.auth.models import User

import datetime
import time
# Create your models here.


class Habit(models.Model):
    """ General timed and checked Habits spanning a selected range of dates.

    Habit will hold data pertaining to it's goal, time spent on the habit, 
    and amount of times the habits's activity has been done. The title 
    will refer to the habit's activity. Each activity has the option of 
    being a timed or a checked. Timed habits will mean the goal is in 
    hours, and checked habits will be whole number increments refering to how 
    many times the habit activity was completed. Each goal will have a type,
    either daily, or total. Total goals will have completed be True
    if current_completed_timed_amount or current_times_activity_done 
    (depending on the type of habit) being greater than the goal amount. 
    If the type of goal is daily, completed will never be true, and 
    whether the daily goal is completed will be handled by the Daily_Habit 
    model. 

    Keyword Arguments
    -----------------
    start_date -- initial date of the habit activities on this date are counted
    end_date   -- last date of the habit activities on this date are counted
    type_of_habit -- either timed or checked
    goal_amount -- amount to achieve goal completed, timed=hrs,checked=times completed
    current_completed_timed_amount -- time duration accumulated from each habit's activity
    current_times_activity_done -- accumulated total number of activities for habit
    completed -- true or false pending if goal_amount is surpassed
    user -- user that made this goal

    Methods
    -------
    check_compeleted: 
        change completed to true if accumulated activity totals greater than the goal_amount. 
    
    create_all_daily_habits:
        if type_of_goal daily, create corresponding Daily_Habit models.
    
    save:
        save the Habit model and call the checked_completed and create_all_daily_habits.

    """
    start_date = models.DateField()
    end_date = models.DateField()
    type_of_habit = models.CharField(max_length=30) # timed, or checked
    title = models.CharField(max_length=100)
    type_of_goal = models.CharField(default='total', max_length=50) # daily goal or total goal
    goal_amount = models.FloatField()
    current_completed_timed_amount = models.DurationField(default=datetime.timedelta(0),null=True, blank=True)
    current_times_activity_done = models.IntegerField(default=0, null=True, blank=True)
    completed = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
 
    def check_completed(self):
        """change completed to true if accumulated activity totals greater than the goal_amount."""

        if self.type_of_habit == 'checked':
            if self.current_times_activity_done >= float(self.goal_amount):
                self.completed = True
            else:
                self.completed = False
        else:
            if float(self.goal_amount) >= 1:
                goal_amount_in_hours = datetime.timedelta(hours=float(self.goal_amount))
            else:
                minutes = float(self.goal_amount) * 60
                goal_amount_in_hours = datetime.timedelta(minutes=minutes)

            if self.current_completed_timed_amount >= goal_amount_in_hours:
                 self.completed = True
            else:
                self.completed = False

    def create_all_daily_habits(self):
        """if type_of_goal daily, create corresponding Daily_Habit models."""
        #get a date for every date in the range of start date to end date 
        datetime_start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') 
        datetime_end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d') 

        difference_dates = datetime_end_date - datetime_start_date 
        difference_dates += datetime.timedelta(days=1)
        all_days = []
        # fill all_days with each date from start_date to end_date 
        while datetime_start_date <= datetime_end_date:
            all_days.append(datetime_start_date)
            datetime_start_date += datetime.timedelta(days=1)
        
        # for each date make a daily_habit_object
        for date in all_days:
            new_daily_habit = Daily_Habit.objects.create(habit=self, date=date)
            new_daily_habit.save()

    def save(self, *args, **kwargs):
        is_new = True if not self.id else False 

        if is_new:
            self.check_completed()
            super(Habit,self).save( *args, **kwargs)
            self.create_all_daily_habits()
        else:
            self.check_completed()
            super(Habit,self).save( *args, **kwargs)


class Daily_Habit(models.Model):
    """A habit pertaining to a specific date, with accumulated totals for that date.
    
    Daily_Habits will accumulate timed and count totals from activity models, 
    these totals will be compared to Habit model goals with a type_of_goal 
    of daily in order to be completed.

    Keyword_Arguments
    -----------------
    date: Day of the Daily_Habit
    timed_total: accumulated timed of the activities for this day for this Habit
    count_times_done_total: total number of ativities for this Habit on this day
    habit: the general habit from which this Daily_Habit is created
    completed: Boolean refering to if the habit goal was reached for this date

    Methods
    --------
    check_completed:
       Make the completed argument value True if habit goal accomplished for this date.

    save:
        Call checked_completed method if habit.type_of_goal is daily and save instances.

    """
    date = models.DateField(null=True, blank=True)
    timed_total = models.DurationField(default = datetime.timedelta(0),null=True, blank=True)
    count_times_done_total = models.PositiveIntegerField(default=0, null=True, blank=True)
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE,null=True, blank=True)
    completed = models.BooleanField(default = False)

    def check_completed(self):
        """Make the completed argument value True if habit goal accomplished for this date."""

        if self.habit.type_of_habit == 'timed':
            if float(self.habit.goal_amount) >= 1:
                goal_amount_in_time_metric = datetime.timedelta(hours=float(self.habit.goal_amount))
            else:
                minutes = float(self.habit.goal_amount) * 60
                goal_amount_in_time_metric = datetime.timedelta(minutes=minutes)
            
            if self.timed_total >= goal_amount_in_time_metric:
                self.completed = True
            else:
                self.completed = False
        
        else:
            if self.count_times_done_total >= float(self.habit.goal_amount):
                self.completed = True
            else:
                self.completed = False

    def save(self, *args, **kwargs):
        """Call checked_completed method if habit.type_of_goal is daily and save instances."""

        if self.habit.type_of_goal == 'daily':
            self.check_completed()
        else:
            pass
        super(Daily_Habit,self).save( *args, **kwargs)


class activity(models.Model):
    """Activity that pertains to each Habit Model in order to complete Habit goals.
    
    Each activity will correspond with a habit and last for a duration of time.

    Keyword Arguments
    -----------------
    habit: the specific Habit model this activity is for
    daily_habit: the specific Daily_habit this activity is for
    start_time: the beggining time of this habit
    end_time: the end time of the habit
    total_time: the difference between the start_time and end_time

    Methods
    -------
    create_total_time: 
        Return the difference between activity start_time and end_time.

    create_end_time:
        For checked habits, create an end_time of 4 minutes from start_time.
    
    add_data_to_daily_habit_date:
        Add the activity information to the corresponding daily_habit.

    save:
        Update Habit and Daily_Habit models with activity data.

    """
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    daily_habit = models.ForeignKey(Daily_Habit, on_delete=models.CASCADE,null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)


    def create_total_time(self):
        """Return the difference between activity start_time and end_time."""

        if self.end_time:
            self.total_time = self.end_time - self.start_time 
            return self.total_time
        else:
            pass
    
    #all checked habits will have an end time of 10 minutes after start time
    def create_end_time(self):
        """For checked habits create an end_time of 4 minutes from start_time."""

        new_minutes = datetime.timedelta(minutes=4)
        new_end_time = self.start_time + new_minutes
        self.end_time = new_end_time
        

    def add_data_to_daily_habit_date(self,date, count=False):
        """Add the activity information to the corresponding daily_habit."""
        this_daily_habit = Daily_Habit.objects.filter(habit=self.habit).filter(date=date)
        if  this_daily_habit:
            this_daily_habit = this_daily_habit[0]

            # if it is a timed habit then add 
            total_time = self.create_total_time()
            if total_time:
                this_daily_habit.timed_total += total_time

            # dont count an activity to be done twice 
            if count == True:
                this_daily_habit.count_times_done_total += 1
            this_daily_habit.save()
        else:
            pass


    def save(self, *args, **kwargs):
        """Update Habit and Daily_Habit models with activity data."""
        ## update the habits  current_completed_timed_amount or 
        ## current_times_activity_done
        ## always update times done 
        day = str(self.start_time.date())
        ## add an end time to only checked habit activities
        if self.habit.type_of_habit == 'checked':
            self.create_end_time()
            self.create_total_time()
        else:
            pass
        
        is_new = True if not self.id else False 
        if is_new:
            self.habit.current_times_activity_done += 1
            self.add_data_to_daily_habit_date(day, count=True)
            ## just get the day from datetime 
            #if habit is timed then add the total_time to the total_time completed
            self.habit.save()
        else:
            self.add_data_to_daily_habit_date(day, count=False)
            if self.habit.type_of_habit == 'timed' and self.end_time:
                # if its the first time activity for this habit then set timed_amount to this
                self.create_total_time()
                if self.habit.current_completed_timed_amount == None:
                    self.habit.current_completed_timed_amount = self.total_time
                else:
                    self.habit.current_completed_timed_amount += self.total_time

                # now update totals for daily 
                self.habit.save()
            else:
                pass
            
        super(activity,self).save( *args, **kwargs)

    # when it gets saved generate the total_time field?


