from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
   
class auction_list(models.Model):
    title = models.CharField(max_length=50)
    descrption = models.CharField(max_length=4000)
    image = models.CharField(max_length=1000)
    isactive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name="user")

    def __str__(self):
        return f"Title: {self.title}    Written by: {self.owner}"