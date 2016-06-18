from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User)
    balance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class Transaction(models.Model):
    recepient = models.ForeignKey(Account)
    description = models.TextField(max_length=400,blank=True)
    value = models.IntegerField(default=0)
    last_modified_date = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        print self.last_modified_date
        return self.recepient.user.username + " " + str(self.value)


