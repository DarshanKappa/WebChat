from django.db import models
from django.db.models.fields import BooleanField

# Create your models here.

class chat_list(models.Model):
    
    
    user_id = models.IntegerField(default='1')
    second_user_id = models.IntegerField()
    user_want = models.BooleanField(default=False)
    second_user_want = BooleanField(default=False)

    

class chat(models.Model):

    chat_id = models.IntegerField()
    message = models.TextField(max_length=1000,default="")
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    


