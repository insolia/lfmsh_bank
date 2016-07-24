from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Account(models.Model):
    '''
    Extension of a user class
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

    def lab_needed(self):
        if self.grade < 9:
            return 3
        return 2

    def fac_needed(self):
        if self.grade < 9:
            return 0
        return 1

    def sem_read(self):
        a = Transaction.objects.filter(recipient=self.user, type=TransactionType.objects.get(name='Seminar'), value__gte=0)
        return len(a)


    def can_add_trans(self):
        if self.user.groups.filter(name__in=['pedsostav', 'admin']):
            return True
        return False


    def get_balance(self):
        return self.balance


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

    recipient = models.ForeignKey(User, related_name='received_trans', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='created_trans', on_delete=models.CASCADE)

    description = models.TextField(max_length=400, blank=True)
    value = models.IntegerField(default=0)

    counted = models.BooleanField(default=False, editable=False)

    type = models.ForeignKey(TransactionType)
    status = models.ForeignKey(TransactionStatus)

    modifier = models.ForeignKey(User, blank=True, null=True, related_name='modified_trans')
    last_modified_date = models.DateTimeField(blank=True, null=True)


    def __unicode__(self):
        return self.recipient.username + " " + str(self.value)

    @classmethod
    def create_trans(cls, recipient, value, creator, description, type, status):

        if 'pioner' in creator.groups.filter(name__in=['pioner']) and type.name != 'p2p':
            raise StandardError('While creating transaction. Pioner tried to create not p2p trans ')

        new_trans = cls(recipient=recipient, value=value, creator=creator, description=description,
                        type=type, status=status)

        if status.name == 'PR':
            new_trans.count()
        else:
            new_trans.save()

        if type.name == 'fac_pass':
            a = new_trans.recipient.account
            a.fac_passed += 1
            a.save()

        if type.name == 'lab_pass':
            a = new_trans.recipient.account
            a.lab_passed += 1
            a.save()

        return new_trans


    def count(self):

        if self.counted:
            return False

        a = self.recipient.account
        a.balance = a.balance + self.value
        a.save()

        a = self.creator.account
        a.balance = a.balance - self.value
        a.save()

        self.counted = True
        self.save()
        return True


    def cancel(self):

        if not self.counted:
            return False

        a = self.recipient.account
        a.balance = a.balance - self.value
        a.save()

        a = self.creator.account
        a.balance = a.balance + self.value
        a.save()

        self.counted = False
        self.save()
        return True


    def can_be_declined(self):
        if self.status.name in ['DA', 'DC']:
            return False
        if self.type.name == 'p2p' and self.status.name == 'PR':
            return False
        return True

    def get_creation_date(self):
        return self.creation_date.strftime("%d.%m.%Y %H:%M")

