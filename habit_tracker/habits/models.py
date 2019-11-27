from django.db import models

from django.contrib.auth.models import User

import datetime
import time
# Create your models here.


class Habit(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    type_of_habit = models.CharField(max_length=30) # will be select option 
    title = models.CharField(max_length=100)
    type_of_goal = models.CharField(default='total', max_length=50) #goal can be daily goal or total goal
    goal_amount = models.FloatField()
    current_completed_timed_amount = models.DurationField(default=datetime.timedelta(0),null=True, blank=True)
    current_times_activity_done = models.IntegerField(default=0, null=True, blank=True)
    completed = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
 
    def check_completed(self):
        if self.type_of_habit == 'checked':
            if self.current_times_activity_done >= float(self.goal_amount):
                self.completed = True
            else:
                self.completed = False
        else:
            if float(self.goal_amount) >= 1:
                goal_amount_in_hours = datetime.timedelta(hours=float(self.goal_amount))
            else:
                goal_amount_in_hours = datetime.timedelta(minutes=float(self.goal_amount))

            if self.current_completed_timed_amount >= goal_amount_in_hours:
                 self.completed = True
            else:
                self.completed = False
    
        

    def create_all_daily_habits(self):
        # for get a a date for every date in the range of start date to end date 
        
        #base = self.end_date - self.start_date
        #print(self.start_date, self.end_date )
        
        datetime_start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') 
        datetime_end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d') 

        difference_dates = datetime_end_date - datetime_start_date 
        difference_dates += datetime.timedelta(days=1)
        #print(base.days)
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
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django

        if is_new:
            self.check_completed()
            super(Habit,self).save( *args, **kwargs)
            self.create_all_daily_habits()
        else:
            self.check_completed()
            super(Habit,self).save( *args, **kwargs)


class Daily_Habit(models.Model):
    date = models.DateField(null=True, blank=True)
    timed_total = models.DurationField(default = datetime.timedelta(0),null=True, blank=True)
    count_times_done_total = models.PositiveIntegerField(default=0, null=True, blank=True)
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE,null=True, blank=True)
    completed = models.BooleanField(default = False)

    def check_completed(self):
        if self.habit.type_of_habit == 'timed':
            if float(self.habit.goal_amount) >= 1:
                goal_amount_in_time_metric = datetime.timedelta(hours=float(self.habit.goal_amount))
            else:
                goal_amount_in_time_metric = datetime.timedelta(minutes=float(self.habit.goal_amount))
            
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
        if self.habit.type_of_goal == 'daily':
            self.check_completed()
        else:
            pass
        super(Daily_Habit,self).save( *args, **kwargs)


class activity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    daily_habit = models.ForeignKey(Daily_Habit, on_delete=models.CASCADE,null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)


    def create_total_time(self):
        if self.end_time:
            self.total_time = self.end_time - self.start_time 
            return self.total_time
        else:
            pass
    
    #all checked habits will have an end time of 10 minutes after start time
    def create_end_time(self):
        print(self.start_time)
        new_minutes = self.start_time.minute + 10
        new_end_time = self.start_time.replace(minute = new_minutes )
        
        self.end_time = new_end_time
        print(self.end_time)
        

    def add_data_to_daily_habit_date(self,date, count=False):
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
        
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
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


