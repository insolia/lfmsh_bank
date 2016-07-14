from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Account(models.Model):
    '''
    Extention of a user class
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    balance = models.IntegerField(default=0)
    third_name = models.CharField(max_length=40, default='Not stated')

    otr = models.IntegerField(default=1)

    grade = models.IntegerField(blank=True, default=8)
    lab_passed = models.IntegerField(blank=True, default=0)
    fac_passed = models.IntegerField(blank=True, default=0)
    sem_attend = models.IntegerField(blank=True, default=0)


    def __unicode__(self):
        if self.user.first_name:

            return self.user.last_name + ' ' + self.user.first_name[0] + '. ' + self.third_name[0] + '.'
        else:
            return self.user.last_name

    def long_name(self):
        return self.user.last_name + ' ' + self.user.first_name + ' ' + self.third_name

    def short_name(self):
        if self.user.first_name:

            return self.user.last_name + ' ' + self.user.first_name[0] + '. ' + self.third_name[0] + '.'
        else:
            return self.user.last_name


    def can_add_trans(self):
        if self.user.groups.filter(name__in=['pedsostav', 'admin']):
            return True
        return False


class TransactionType(models.Model):
    name = models.CharField(max_length=30)
    human_name = models.CharField(max_length=30, default='Other')
    group1 = models.CharField(max_length=30, blank=True, null=True)
    group2 = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.human_name


class TransactionStatus(models.Model):
    name = models.CharField(max_length=30)
    human_name = models.CharField(max_length=30)
    counted = models.BooleanField(default=False)
    group1 = models.CharField(max_length=30, blank=True, null=True)
    group2 = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.human_name


class Transaction(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    recipient = models.ForeignKey(User, related_name='received_trans')
    creator = models.ForeignKey(User, related_name='created_trans')

    description = models.TextField(max_length=400, blank=True)
    value = models.IntegerField(default=0)

    counted = models.BooleanField(default=False, editable=False)

    type = models.ForeignKey(TransactionType)
    status = models.ForeignKey(TransactionStatus)

    modifier = models.ForeignKey(User, blank=True, null=True, related_name='modified_trans')
    last_modified_date = models.DateTimeField(blank=True, null=True)


    def __unicode__(self):
        return self.recipient.username + " " + str(self.value)

    def count(self):

        if self.counted:
            return False

        a = self.recipient.account
        a.balance = a.balance + self.value
        a.save()

        # here should be if type = p2p: creator balance substract

        self.counted = True
        self.save()
        return True

    def cancel(self):

        if not self.counted:
            return False

        a = self.recipient.account
        a.balance = a.balance - self.value
        a.save()

        # here should be if type = p2p: creator balance add

        self.counted = False
        self.save()
        return True


    def can_be_declined(self):
        if self.status.name in ['DA', 'DC']:
            return False
        return True

    def get_creation_date(self):
        return self.creation_date.strftime("%d.%m.%Y %H:%M")