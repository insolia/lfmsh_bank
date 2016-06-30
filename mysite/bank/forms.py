from django import forms
from .models import Transaction, Account
from django.contrib.auth.models import User, Group


class SprecialTransForm(forms.Form):
    '''
    class Meta:
        model = Transaction
        fields = ('recipient', 'value', 'description')
    '''

    recipient = forms.ModelChoiceField(queryset=Account.objects.filter(user__groups__name='pioner'))

    description = forms.CharField(max_length=400, widget=forms.Textarea)

    value = forms.IntegerField(label='sum')


class SeminarTransForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=Account.objects.filter(user__groups__name='pioner'))

    description = forms.CharField(label='topic and description', max_length=400, widget=forms.Textarea)

    score = forms.IntegerField(label='score 0-40', max_value=40)