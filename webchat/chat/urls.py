from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('friend_list/', views.friend_list, name="friend_list"),
   path('send_request/', views.send_request, name="send_request"),
   path('accept_request/', views.accept_request, name="accept_request"),
   path('chats/', views.chats, name="chats"),
   path('sendmessage/', views.sendmessage, name="sendmessage"),
   path('allchat/', views.allchat, name="allchat"),
   path('refreshchat/', views.refreshchat, name="refreshchat"),
]