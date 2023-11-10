from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room "),
    path('create-room/', views.createRoom, name="create-room"),

]
