from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.account, name="account"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]