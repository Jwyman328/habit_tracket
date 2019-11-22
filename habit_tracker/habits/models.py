from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Habit(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    type_of_habit = models.CharField(max_length=30) # will be select option 
    title = models.CharField(max_length=100)
    type_of_goal = models.CharField(default='total', max_length=50) #goal can be daily goal or total goal
    goal_amount = models.PositiveIntegerField()
    current_completed_timed_amount = models.DurationField(null=True, blank=True)
    current_times_activity_done = models.IntegerField(default=0, null=True, blank=True)

    completed = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class activity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)

    def create_total_time(self):
        self.total_time = self.end_time - self.start_time 
        return self.total_time

    def save(self, *args, **kwargs):
        ## update the habits  current_completed_timed_amount or 
        ## current_times_activity_done
        ## always update times done 
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
        if is_new:
            self.habit.current_times_activity_done += 1
            self.habit.save()
        else:
            pass
        super(activity,self).save( *args, **kwargs)

    # when it gets saved generate the total_time field?


