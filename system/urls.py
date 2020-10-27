from django.contrib import admin
from django.urls import path, include

from system import views

urlpatterns = [
    path('slider/list/', views.slider_list,name='slider_list'),

]