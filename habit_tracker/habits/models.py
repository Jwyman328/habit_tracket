from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Habit(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    type_of_habit = models.CharField(max_length=30) # will be select option 
    title = models.CharField(max_length=100)
    goal_amount = models.PositiveIntegerField()
    completed = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class activity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_time = models.FloatField(default = 0)

    def create_total_time(self):
        self.total_time = self.end_time - self.start_time 
        return self.total_time

    # when it gets saved generate the total_time field?

