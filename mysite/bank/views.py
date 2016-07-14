from django.shortcuts import render
from django.http import HttpResponse
from bank.models import Account, Transaction, TransactionType, TransactionStatus
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

    print request.user.account.can_add_trans()

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name
    print user_group_name
    return render(request, 'bank/indexx.html', {'user_group': user_group_name})


def all_pioner_accounts(request):
    template_name = 'bank/user_lists/pioner_list.html'

    accounts = {}
    accounts['1'] = Account.objects.filter(user__groups__name='pioner').filter(otr=1)
    accounts['2'] = Account.objects.filter(user__groups__name='pioner').filter(otr=2)
    accounts['3'] = Account.objects.filter(user__groups__name='pioner').filter(otr=3)
    accounts['4'] = Account.objects.filter(user__groups__name='pioner').filter(otr=4)

    return render(request, template_name, {'accounts': accounts})

def all_ped_accounts(request):
    template_name = 'bank/user_lists/ped_list.html'
    accounts = Account.objects.filter(user__groups__name='pedsostav').order_by('-balance')
    return render(request, template_name, {'accounts': accounts})


def show_my_trans(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))


    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    out_trans = Transaction.objects.filter(creator=request.user).order_by('-creation_date')

    if user_group_name == 'pioner':

        in_trans = Transaction.objects.filter(recipient=request.user).order_by('-creation_date')

        return render(request, 'bank/transaction_lists/my_trans_list_pioner.html',
                      {'in_trans': in_trans, 'out_trans': out_trans})
    else:
        return render(request, 'bank/transaction_lists/my_trans_list_ped.html',
                      {'out_trans': out_trans})

def add_special(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

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
            status = TransactionStatus.objects.get(name='PR')

            new_trans = Transaction(recipient=recipient, value=value, creator=creator, description=description,
                                    type=type, status=status)

            new_trans.count()

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_special.html', {'form': form})


    else:

        form = SprecialTransForm()
        return render(request, 'bank/add_trans/trans_add_special.html', {'form': form})


def add_zaryadka(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

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

        status = TransactionStatus.objects.get(name='PR')



        new_transactions = []
        for u in zar_attendants:
            new_trans = Transaction(recipient=u, value=value, creator=creator, description=description,
                                    type=type, status=status)
            new_trans.count()
            new_transactions.append(new_trans)

        if new_transactions:
            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': new_transactions})

        else:
            users = User.objects.filter(groups__name='pioner')
            return render(request, 'bank/add_trans/trans_add_zaryadka.html', {'users': users})
    else:
        users = {}
        users['1'] = User.objects.filter(groups__name='pioner').filter(account__otr=1)
        users['2'] = User.objects.filter(groups__name='pioner').filter(account__otr=2)
        users['3'] = User.objects.filter(groups__name='pioner').filter(account__otr=3)
        users['4'] = User.objects.filter(groups__name='pioner').filter(account__otr=4)

        return render(request, 'bank/add_trans/trans_add_zaryadka.html', {'users': users})


def add_sem(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        form = SeminarTransForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']

            value = hf.seminar(score)
            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='Seminar')
            status = TransactionStatus.objects.get(name='PR')

            new_trans = Transaction(recipient=recipient, value=value, creator=creator, description=description,
                                    type=type, status=status)

            new_trans.count()

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_seminar.html', {'form': form})


    else:

        form = SeminarTransForm()
        return render(request, 'bank/add_trans/trans_add_seminar.html', {'form': form})


def dec_trans(request, trans_id):
    print 'decline page'
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    trans = Transaction.objects.get(pk=trans_id)
    if trans.creator != request.user and user_group_name != 'admin':
        return redirect(reverse('bank:index'))

    return render(request, 'bank/dec_trans/trans_dec_confirm.html', {'t': trans})


def dec_trans_ok(request, trans_id):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name
    trans = Transaction.objects.get(pk=trans_id)
    if trans.creator != request.user and user_group_name != 'admin':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        # decline of trans happening
        trans.cancel()
        if user_group_name == 'admin':
            trans.status = TransactionStatus.objects.get(name='DA')

        else:
            trans.status = TransactionStatus.objects.get(name='DC')

        trans.save()



    else:
        return redirect(reverse('bank:index'))

    return render(request, 'bank/dec_trans/trans_dec_ok.html', {'transactions': [trans]})


def trans_list(request, username):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name
    if user_group_name != 'admin':
        return redirect(reverse('bank:index'))

    t_user = User.objects.get(username=username)

    in_trans = Transaction.objects.filter(recipient=t_user).order_by('-last_modified_date')
    out_trans = Transaction.objects.filter(creator=t_user).order_by('-last_modified_date')

    return render(request, 'bank/transaction_lists/admin_trans_list.html',
                  {'in_trans': in_trans, 'out_trans': out_trans, 'user_group': user_group_name, 'user': t_user})


