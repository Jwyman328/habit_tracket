"""habit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('<int:id>/', views.individual_habit_view.as_view(), name='individual_habit'),
    path('<int:habit_id>/<int:year>/<int:month>/<int:day>',views.habit_total_acumulated_for_specific_date.as_view(),name = 'habit_total_acumulated_for_specific_date'),
    path('<int:habit_id>/activities/<int:year>/<int:month>/<int:day>/', views.individual_habit_date_activity_view.as_view(), name='individual_habit_date_activity'),
    path('activities/<int:year>/<int:month>/<int:day>/', views.all_completed_activities_for_date.as_view(), name='all_activities_for_date'),
    path('activities/timed/<int:year>/<int:month>/<int:day>/', views.timed_activities_for_date.as_view(), name='timed_activities_for_date'),
    path('activities/checked/<int:year>/<int:month>/<int:day>/', views.checked_activities_for_date.as_view(), name='checked_activities_for_date'),

    path('activities/update/<int:activity_id>/<int:year>/<int:month>/<int:day>/<int:hr>/<int:minute>/<int:sec>/', views.update_activity_end_time.as_view(), name='update_activity_end_time'),
    path('<int:id>/activities/', views.individual_habit_activity_list.as_view(), name='individual_habit_activity_list'),
    path('activity/<int:id>/', views.individual_activity.as_view(), name='individual_activity'),
    path('create_habit', views.create_habit.as_view(), name='create_habit' ),
    path('create_activity', views.create_activity.as_view(), name='create_activity'),
    path('<int:year>/<int:month>/<int:day>/',views.all_habits_for_specific_date.as_view(), name='all_habits_for_specific_date' ),
    path('daily_habits/<int:id>/', views.specific_daily_habit_data.as_view(), name='specific_daily_habit_data'),
    path('daily_habits/<int:year>/<int:month>/<int:day>/', views.daily_habits_by_date.as_view(), name='daily_habits_by_date'),


]
