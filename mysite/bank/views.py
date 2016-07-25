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
from .forms import *
from django_tables2 import RequestConfig
from .tables import *
from django.utils import timezone
import helper_functions as hf




# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    print request.user.account.can_add_trans()

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name
    p2p_unmanaged_len = len(Transaction.objects.filter(status__name='AD'))
    print user_group_name
    return render(request, 'bank/indexx.html', {'user_group': user_group_name, 'unm_len': p2p_unmanaged_len, 'p2p_buf':hf.p2p_buf})


def all_pioner_accounts(request):
    template_name = 'bank/user_lists/pioner_list.html'

    accounts = {}
    accounts['1'] = Account.objects.filter(user__groups__name='pioner').filter(otr=1).order_by('user__last_name')
    accounts['2'] = Account.objects.filter(user__groups__name='pioner').filter(otr=2).order_by('user__last_name')
    accounts['3'] = Account.objects.filter(user__groups__name='pioner').filter(otr=3).order_by('user__last_name')
    accounts['4'] = Account.objects.filter(user__groups__name='pioner').filter(otr=4).order_by('user__last_name')

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
            type = form.cleaned_data['type']

            status = TransactionStatus.objects.get(name='PR')

            new_trans = Transaction.create_trans(recipient=recipient, value=value, creator=creator,
                                                 description=description,
                                                 type=type, status=status)

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_special.html', {'form': form})


    else:

        form = SprecialTransForm()
        return render(request, 'bank/add_trans/trans_add_special.html', {'form': form})


def add_mass_special(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":
        print request.POST['type']

        fac_attendants = []
        form = SprecialTransForm(request.POST)

        for u in User.objects.filter(groups__name='pioner'):
            if u.username + '_num' in request.POST and request.POST[u.username + '_num']:
                fac_attendants.append((u, request.POST[u.username + '_num']))

        if not fac_attendants:
            return redirect(reverse('bank:index'))

        creator = request.user

        description = request.POST['description']
        type = TransactionType.objects.get(pk = request.POST['type'])

        print type
        status = TransactionStatus.objects.get(name='PR')
        new_transactions = []
        for u, s in fac_attendants:
            new_trans = Transaction.create_trans(recipient=u, value=int(s), creator=creator, description=description,
                                             type=type, status=status)
            new_transactions.append(new_trans)
        if new_transactions:
            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': new_transactions})
        else:
            users = User.objects.filter(groups__name='pioner')
            return render(request, 'bank/add_trans/trans_add_mass_special.html', {'users': users})





    else:
        users = {}
        users['1'] = User.objects.filter(groups__name='pioner').filter(account__otr=1).order_by('last_name')
        users['2'] = User.objects.filter(groups__name='pioner').filter(account__otr=2).order_by('last_name')
        users['3'] = User.objects.filter(groups__name='pioner').filter(account__otr=3).order_by('last_name')
        users['4'] = User.objects.filter(groups__name='pioner').filter(account__otr=4).order_by('last_name')

        form = SprecialTransForm()

        return render(request, 'bank/add_trans/trans_add_mass_special.html', {'users': users, 'form': form})


def add_zaryadka(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":
        print request.POST
        if len(request.POST) < 3:
            return redirect(reverse('bank:index'))

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
            new_trans = Transaction.create_trans(recipient=u, value=value, creator=creator, description=description,
                                                 type=type, status=status)
            new_transactions.append(new_trans)

        if new_transactions:
            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': new_transactions})

        else:
            users = User.objects.filter(groups__name='pioner')
            return render(request, 'bank/add_trans/trans_add_zaryadka.html', {'users': users})
    else:
        users = {}
        users['1'] = User.objects.filter(groups__name='pioner').filter(account__otr=1).order_by('last_name')
        users['2'] = User.objects.filter(groups__name='pioner').filter(account__otr=2).order_by('last_name')
        users['3'] = User.objects.filter(groups__name='pioner').filter(account__otr=3).order_by('last_name')
        users['4'] = User.objects.filter(groups__name='pioner').filter(account__otr=4).order_by('last_name')

        return render(request, 'bank/add_trans/trans_add_zaryadka.html', {'users': users})


def add_fac(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":
        print request.POST

        fac_attendants = []

        for u in User.objects.filter(groups__name='pioner'):
            if u.username + '_num' in request.POST and request.POST[u.username + '_num']:
                fac_attendants.append((u, request.POST[u.username + '_num']))

        if not fac_attendants:
            return redirect(reverse('bank:index'))

        description = request.POST['description']
        creator = request.user
        type = TransactionType.objects.get(name='fac_pass')

        status = TransactionStatus.objects.get(name='PR')

        new_transactions = []
        for u, s in fac_attendants:
            new_trans = Transaction.create_trans(recipient=u, value=int(s), creator=creator, description=description,
                                                 type=type, status=status)
            new_transactions.append(new_trans)

        if new_transactions:
            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': new_transactions})

        else:
            users = User.objects.filter(groups__name='pioner')
            return render(request, 'bank/add_trans/trans_add_fac.html', {'users': users})
    else:
        users = {}
        users['1'] = User.objects.filter(groups__name='pioner').filter(account__otr=1).order_by('last_name')
        users['2'] = User.objects.filter(groups__name='pioner').filter(account__otr=2).order_by('last_name')
        users['3'] = User.objects.filter(groups__name='pioner').filter(account__otr=3).order_by('last_name')
        users['4'] = User.objects.filter(groups__name='pioner').filter(account__otr=4).order_by('last_name')

        return render(request, 'bank/add_trans/trans_add_fac.html', {'users': users})


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

            new_trans = Transaction.create_trans(recipient=recipient, value=value, creator=creator,
                                                 description=description,
                                                 type=type, status=status)

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_seminar.html', {'form': form})


    else:

        form = SeminarTransForm()
        return render(request, 'bank/add_trans/trans_add_seminar.html', {'form': form})


def add_lab(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name == 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        form = LabTransForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='lab_pass')
            status = TransactionStatus.objects.get(name='PR')

            new_trans = Transaction.create_trans(recipient=recipient, value=value, creator=creator,
                                                 description=description,
                                                 type=type, status=status)

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_lab.html', {'form': form})


    else:

        form = LabTransForm()
        return render(request, 'bank/add_trans/trans_add_lab.html', {'form': form})


def add_p2p(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name != 'pioner':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        form = P2PTransForm(request.POST, max_value=int(request.user.account.balance - hf.p2p_buf))
        form.fields['value'].max_value = int((request.user.account.balance * hf.p2p_proc))
        print form.fields['value'].max_value
        print form.fields['value']


        if form.is_valid():
            value = form.cleaned_data['value']
            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='p2p')
            status = TransactionStatus.objects.get(name='AD')

            new_trans = Transaction.create_trans(recipient=recipient, value=value, creator=creator,
                                                 description=description, type=type, status=status)

            return render(request, 'bank/add_trans/trans_add_p2p_ok.html', {'a': new_trans})
        return render(request, 'bank/add_trans/trans_add_p2p.html', {'form': form})


    else:

        form = P2PTransForm(int((request.user.account.balance - hf.p2p_buf)))
        form.fields['recipient'].queryset = form.fields['recipient'].queryset.exclude(user=request.user)

        print form.fields['value'].max_value

        return render(request, 'bank/add_trans/trans_add_p2p.html', {'form': form})


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
        trans.cancel

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

    in_trans = Transaction.objects.filter(recipient=t_user).order_by('-creation_date')
    out_trans = Transaction.objects.filter(creator=t_user).order_by('-creation_date')

    return render(request, 'bank/transaction_lists/admin_trans_list.html',
                  {'in_trans': in_trans, 'out_trans': out_trans, 'user_group': user_group_name, 'user': t_user})


def manage_p2p(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name != 'admin':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        print(request.POST)

        con_trans = []
        dec_trans = []

        for pk in xrange(1000):
            if 'c_' + str(pk) in request.POST:
                t = Transaction.objects.get(pk=pk)
                if request.POST['c_'+str(pk)] == 'confirm':
                    print 'confirm' + str(t.pk)
                    t.status = TransactionStatus.objects.get(name='PR')
                    t.count()

                    con_trans.append(t)

                if request.POST['c_'+str(pk)] == 'cancel':
                    print 'cancel' + str(t.pk)
                    t.status = TransactionStatus.objects.get(name='DA')
                    t.save()
                    dec_trans.append(t)

    trans = Transaction.objects.filter(status__name='AD').order_by('creation_date')

    return render(request, 'bank/transaction_lists/admin_p2p_list.html', {'trans': trans})


def super_table(request):
    table = TransTable(Transaction.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'bank/s_table.html', {'trans': table})



