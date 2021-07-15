from django.contrib import admin
from .models import chat_list, chat

# Register your models here.

admin.site.register(chat_list)
admin.site.register(chat)

