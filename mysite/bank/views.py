from django.shortcuts import render
from django.http import HttpResponse
from bank.models import Account, Transaction, TransactionType
from django.template import Context, loader
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import logout_then_login
from django.views import generic
from django.core.urlresolvers import reverse
from .forms import SprecialTransForm, SeminarTransForm
from django.utils import timezone
import helper_functions as hf




# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    return render(request, 'bank/index.html', {'user_group': user_group_name})


class all_accounts_view(generic.ListView):
    template_name = 'bank/show_all.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user__groups__name='pioner').order_by('-balance')


def show_my_trans(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    in_trans = Transaction.objects.filter(recipient=request.user).order_by('-last_modified_date')
    out_trans = Transaction.objects.filter(creator=request.user).order_by('-last_modified_date')
    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    return render(request, 'bank/trans_list.html',
                  {'in_trans': in_trans, 'out_trans': out_trans, 'user_group': user_group_name})


def add_special(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        form = SprecialTransForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='Other')

            new_trans = Transaction(recipient=recipient, value=value, creator=creator, description=description,
                                    type=type, status='CO')

            new_trans.count()

            return render(request, 'bank/trans_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/trans_add_special.html', {'form': form})


    else:

        form = SprecialTransForm()
        return render(request, 'bank/trans_add_special.html', {'form': form})


def add_zaryadka(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        zar_attendants = []

        for u in User.objects.filter(groups__name='pioner'):
            if u.username + '_check' in request.POST:
                zar_attendants.append(u)

        value = hf.zaryadka(len(zar_attendants))
        description = request.POST['description']
        creator = request.user
        type = TransactionType.objects.get(name='Zaryadka')

        new_transactions = []
        for u in zar_attendants:
            new_trans = Transaction(recipient=u, value=value, creator=creator, description=description,
                                    type=type, status='CO')
            new_trans.count()
            new_transactions.append(new_trans)

        if new_transactions:
            return render(request, 'bank/trans_ok.html', {'transactions': new_transactions})

        else:
            users = User.objects.filter(groups__name='pioner')
            return render(request, 'bank/trans_add_zaryadka.html', {'users': users})
    else:

        users = User.objects.filter(groups__name='pioner')
        return render(request, 'bank/trans_add_zaryadka.html', {'users': users})


def add_sem(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        form = SeminarTransForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']

            ### reprocess score to money
            value = score // 2
            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='Seminar')

            new_trans = Transaction(recipient=recipient, value=value, creator=creator, description=description,
                                    type=type)

            new_trans.count()

            return render(request, 'bank/trans_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/trans_add_seminar.html', {'form': form})


    else:

        form = SeminarTransForm()
        return render(request, 'bank/trans_add_seminar.html', {'form': form})

