from django.db import models

from django.contrib.auth.models import User

#fix to flaw 2
"""class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.IntegerField()"""

#comment this out to fix flaw 2
class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    balance = models.IntegerField(null=False, default=0)
