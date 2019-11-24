from django.db import models

from django.contrib.auth.models import User

import datetime
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

    day_times_activity_done = { } #{'date':{total: num. completed:Bool},} 
    day_total_timed_done = { } #{'date':{total: num. completed:Bool},} 
 
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
    
    def check_completed_for_day(self,date):
        if self.type_of_habit == 'checked':
            day_checked_date = self.day_times_activity_done[date]
            if float(day_checked_date['total']) >= float(self.goal_amount):
                day_checked_date['completed'] = True
            else:
                day_checked_date['completed'] = False
        else:
            if float(self.goal_amount) >= 1:
                goal_amount_in_hours = datetime.timedelta(hours=float(self.goal_amount))
            else:
                goal_amount_in_hours = datetime.timedelta(minutes=float(self.goal_amount))

            #self.day_total_timed_done[date] = {}
            #day_timed_total_date = self.day_total_timed_done[date]
            if 'total' in  self.day_total_timed_done[date]:
                if self.day_total_timed_done[date]['total'] >= goal_amount_in_hours:
                    self.day_total_timed_done[date]['completed'] = True
                else:
                    self.day_total_timed_done[date]['completed'] = False
            else:
                self.day_total_timed_done[date]['total'] = datetime.timedelta(0)
        self.save()

    def save(self, *args, **kwargs):
        self.check_completed()
        super(Habit,self).save( *args, **kwargs)


class activity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)


    def create_total_time(self):
        print(self.start_time)
        print(self.end_time)
        if self.end_time:
            self.total_time = self.end_time - self.start_time 
            return self.total_time
        else:
            pass

    def save(self, *args, **kwargs):
        ## update the habits  current_completed_timed_amount or 
        ## current_times_activity_done
        ## always update times done 
        day = str(self.start_time.date())
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
        if is_new:
            self.habit.current_times_activity_done += 1

            ## just get the day from datetime 
            print(self.habit.day_times_activity_done)
            if day in self.habit.day_times_activity_done: 
                self.habit.day_times_activity_done[day]['total'] += 1
            else:
                self.habit.day_times_activity_done[day] = {}
                self.habit.day_times_activity_done[day]['total'] = 1
                
                self.habit.day_total_timed_done[day] = {}
                self.habit.day_total_timed_done[day]['total'] = datetime.timedelta(0)
            #if habit is timed then add the total_time to the total_time completed
            self.habit.save()
        else:
            if self.habit.type_of_habit == 'timed' and self.end_time:
                # if its the first time activity for this habit then set timed_amount to this
                self.create_total_time()
                if self.habit.current_completed_timed_amount == None:
                    self.habit.current_completed_timed_amount = self.total_time
                else:
                    self.habit.current_completed_timed_amount += self.total_time

                # now update totals for daily 
                if day in self.habit.day_total_timed_done:
                    self.habit.day_total_timed_done[day]['total'] += self.total_time
                else:
                    self.habit.day_total_timed_done[day] = {}
                    self.habit.day_total_timed_done[day]['total'] = self.total_time

                self.habit.save()
            else:
                pass
            
            #if self.end_time:
        self.habit.check_completed_for_day(day) 
        super(activity,self).save( *args, **kwargs)

    # when it gets saved generate the total_time field?


