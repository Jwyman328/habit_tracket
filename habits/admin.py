from django.contrib import admin

from .models import Habit, activity, Daily_Habit
# Register your models here.
admin.site.register(Habit)
admin.site.register(activity)
admin.site.register(Daily_Habit)