from django import forms
from .models import Transaction, Account, TransactionType
from django.contrib.auth.models import User, Group
from django.forms import ModelChoiceField
import helper_functions as hf
from dal import autocomplete


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
        queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr', 'user__last_name'))



    description = forms.CharField(max_length=400, widget=forms.Textarea)

    value = forms.IntegerField(label='sum')

    type = forms.ModelChoiceField(queryset=TransactionType.objects.all())


class SeminarTransForm(forms.Form):
    recipient = RecipientModelChoiceField(queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr',
                                                                                                                'user__last_name'))

    description = forms.CharField(label='topic and description', max_length=400, widget=forms.Textarea)

    score = forms.IntegerField(label='score 0-40', max_value=40)


class P2PTransForm(forms.Form):
    '''
    class Meta:
        model = Transaction
        fields = ('recipient', 'value', 'description')
    '''

    recipient = RecipientModelChoiceField(
        queryset=Account.objects.filter(user__groups__name='pioner').order_by('otr', 'user__last_name'))
    description = forms.CharField(max_length=400, widget=forms.Textarea)

    value = forms.IntegerField(label='sum', max_value=hf.max_p2p_sum)
