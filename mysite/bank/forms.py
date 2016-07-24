# coding=utf-8
from django import forms
from .models import Transaction, Account, TransactionType
from django.contrib.auth.models import User, Group
from django.forms import ModelChoiceField
import helper_functions as hf
from dal import autocomplete

# -*- coding: utf-8 -*-


class RecipientModelChoiceField(ModelChoiceField):
    def label_from_instance(self, account):
        return str(account.otr) + ' ' + (account.long_name())


class SprecialTransForm(forms.Form):
    '''
    class Meta:
        model = Transaction
        fields = ('recipient', 'value', 'description')
    '''

    recipient = RecipientModelChoiceField(
        queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr', 'user__last_name'), label=unicode('Получатель','utf-8'))

    description = forms.CharField(max_length=400, widget=forms.Textarea, label=unicode('Описание','utf-8'))

    value = forms.IntegerField(label=unicode('Сумма', 'utf-8'))

    type = forms.ModelChoiceField(queryset=TransactionType.objects.all().exclude(name='p2p'), label=unicode('Тип','utf-8'))



class LabTransForm(forms.Form):


    recipient = RecipientModelChoiceField(
        queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr', 'user__last_name'), label=unicode('Получатель','utf-8'))

    description = forms.CharField(max_length=400, widget=forms.Textarea, label=unicode('Описание','utf-8'))

    value = forms.IntegerField(label=unicode('Сумма', 'utf-8'), min_value=0)


class SeminarTransForm(forms.Form):

    recipient = RecipientModelChoiceField(queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr',
                                                                                                                'user__last_name'),
                                          label=unicode('Пионер', 'utf-8'))

    description = forms.CharField(label=unicode('Тема и описание', 'utf-8'), max_length=400, widget=forms.Textarea)

    score = forms.IntegerField(label=unicode('Оценка [0, 40]', 'utf-8'), max_value=40, min_value=0)


class P2PTransForm(forms.Form):
    '''
    class Meta:
        model = Transaction
        fields = ('recipient', 'value', 'description')
    '''

    recipient = RecipientModelChoiceField(
        queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr', 'user__last_name'), label=unicode('Получатель','utf-8'))
    description = forms.CharField(max_length=400, widget=forms.Textarea, label=unicode('Описание', 'utf-8'))

    value = forms.IntegerField(label=unicode('Сумма', 'utf-8'), min_value=0)
