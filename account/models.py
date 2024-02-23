from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'account')
    profile_pic = models.ImageField(upload_to= 'account/media/uploads/')
    balance = models.IntegerField()

    