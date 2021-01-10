from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserLoginHistory(models.Model):

    ipaddress = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ipaddress

class UserProfile(models.Model):

    University = models.CharField(max_length=50)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)