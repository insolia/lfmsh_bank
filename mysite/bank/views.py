from django.shortcuts import render
from django.http import HttpResponse
from bank.models import Account, Transaction, TransactionType, TransactionStatus
from django.template import Context, loader
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
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
from constants import *




# Create your views here.
@login_required
def index(request):

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name
    print user_group_name
    if user_group_name == 'pioner':
        lec_pen = hf.lec_pen(request.user.account.lec_missed)

        return render(request, 'bank/index_pio.html', {'user_group': user_group_name, 'p2p_buf':hf.p2p_buf, 'lec_pen':lec_pen})
    elif user_group_name == 'pedsostav':
        return render(request, 'bank/indexx.html', {'user_group': user_group_name})


    p2p_unmanaged_len = len(Transaction.objects.filter(status__name='AD'))

    return render(request, 'bank/indexx.html', {'user_group': user_group_name, 'unm_len': p2p_unmanaged_len})

@login_required
@permission_required('bank.view_pio_trans_list')
def all_pioner_accounts(request):

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    template_name = 'bank/user_lists/pioner_list.html'


    table = []

    for i in xrange(NUMBER_OF_OTR):
        table.append(PionerOtrTable(User.objects.filter(groups__name='pioner').filter(account__otr=i+1),order_by='name'))
        RequestConfig(request).configure(table[i])
        table[i].paginate(per_page=100)

    return render(request, template_name, { 'table': table})

@login_required
@permission_required('bank.view_ped_trans_list',login_url='bank:index')
def all_ped_accounts(request):



    template_name = 'bank/user_lists/ped_list.html'
    accounts = Account.objects.filter(user__groups__name='pedsostav').order_by('user__last_name')
    return render(request, template_name, {'accounts': accounts})

@login_required
def show_my_trans(request):


    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    out_trans = Transaction.objects.filter(creator=request.user).order_by('-creation_date')

    if user_group_name == 'pioner':

        in_trans = Transaction.objects.filter(recipient=request.user).order_by('-creation_date')

        return render(request, 'bank/transaction_lists/my_trans_list_pioner.html',
                      {'in_trans': in_trans, 'out_trans': out_trans})
    else:
        return render(request, 'bank/transaction_lists/my_trans_list_ped.html',
                      {'out_trans': out_trans})


@permission_required('bank.add_transaction',login_url='bank:index')
def add_special(request):

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

@permission_required('bank.add_transaction',login_url='bank:index')
def add_mass_special(request):

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

@permission_required('bank.add_transaction',login_url='bank:index')
def add_zaryadka(request):


    if request.method == "POST":

        zar_attendants = []

        for u in User.objects.filter(groups__name='pioner'):
            if u.username + '_check' in request.POST:
                zar_attendants.append(u)

        if not zar_attendants:
            return redirect(reverse('bank:index'))

        value = hf.zaryadka(len(zar_attendants))
        print value
        description = request.POST['description']
        creator = request.user
        type = TransactionType.objects.get(name='zaryadka')

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

        table = []
        for i in xrange(4):
            table.append(ZarTable(User.objects.filter(groups__name='pioner').filter(account__otr=i+1),order_by='name'))
            RequestConfig(request).configure(table[i])
            table[i].paginate(per_page=1000)


        return render(request, 'bank/add_trans/trans_add_zaryadka.html', { 'table':table})


@permission_required('bank.add_transaction',login_url='bank:index')
def add_lec(request):


    if request.method == "POST":

        lec_missers = []

        for u in User.objects.filter(groups__name='pioner'):
            if u.username + '_check' not in request.POST:
                lec_missers.append(u)

        if not lec_missers:
            return redirect(reverse('bank:index'))


        description = request.POST['description']
        creator = request.user
        type = TransactionType.objects.get(name='fine_lec')

        status = TransactionStatus.objects.get(name='PR')

        new_transactions = []
        for u in lec_missers:
            new_trans = Transaction.create_trans(recipient=u, value=hf.lec_pen(u.account.lec_missed), creator=creator, description=description,
                                                 type=type, status=status)
            new_transactions.append(new_trans)

        return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': new_transactions})



    else:

        table = []
        for i in xrange(4):
            table.append(LecTable(User.objects.filter(groups__name='pioner').filter(account__otr=i+1),order_by='name'))
            RequestConfig(request).configure(table[i])
            table[i].paginate(per_page=1000)


        return render(request, 'bank/add_trans/trans_add_lec.html', { 'table':table})


@permission_required('bank.add_transaction',login_url='bank:index')
def add_fac(request):


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
        type = TransactionType.objects.get(name='fac')

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

        return render(request, 'bank/add_trans/trans_add_fac.html', {'users': users, 'table': 'bank/add_trans/otr_tables/fac_table.html', 'list' : [1,2,3,4]})


@permission_required('bank.add_transaction',login_url='bank:index')
def add_activity(request):


    if request.method == "POST":

        participants = {1:[],2:[],3:[],4:[]}
        f = 0


        for u in User.objects.filter(groups__name='pioner'):
            if str(u.pk) + '_place' in request.POST and request.POST[str(u.pk) + '_place']and int(request.POST[str(u.pk) + '_place']) != 5:

                f = 1
                participants[int(request.POST[str(u.pk) + '_place'])].append(u)

        if not f:
            return redirect(reverse('bank:index'))

        description = request.POST['description']
        creator = request.user
        type = TransactionType.objects.get(name=request.POST['type'])

        status = TransactionStatus.objects.get(name='PR')
        activity_money = {1: int(request.POST['1m']),2:int(request.POST['2m']),3:int(request.POST['3m']),4:int(request.POST['4m'])}
        new_transactions = []
        for p in participants:

            for u in participants[p]:
                new_trans = Transaction.create_trans(recipient=u, value=activity_money[p], creator=creator, description=description,
                                                 type=type, status=status)
                new_transactions.append(new_trans)

        if new_transactions:
            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': new_transactions})

        else:
            users = User.objects.filter(groups__name='pioner')
            return render(request, 'bank/add_trans/trans_add_activity.html', {'users': users})
    else:
        users = {}
        users['1'] = User.objects.filter(groups__name='pioner').filter(account__otr=1).order_by('last_name')
        users['2'] = User.objects.filter(groups__name='pioner').filter(account__otr=2).order_by('last_name')
        users['3'] = User.objects.filter(groups__name='pioner').filter(account__otr=3).order_by('last_name')
        users['4'] = User.objects.filter(groups__name='pioner').filter(account__otr=4).order_by('last_name')

        return render(request, 'bank/add_trans/trans_add_activity.html', {'users': users, 'table': 'bank/add_trans/otr_tables/activity_table.html', 'list' : [1,2,3,4], 'activity': ACTIVITY_MONEY})

@permission_required('bank.add_transaction',login_url='bank:index')
def add_sem(request):

    if request.method == "POST":

        form = SeminarTransForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']

            value = hf.seminar(score)

            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='sem')
            status = TransactionStatus.objects.get(name='PR')

            new_trans = Transaction.create_trans(recipient=recipient, value=value, creator=creator,
                                                 description=description,
                                                 type=type, status=status)

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_seminar.html', {'form': form})


    else:

        form = SeminarTransForm()
        return render(request, 'bank/add_trans/trans_add_seminar.html', {'form': form})

@permission_required('bank.add_transaction',login_url='bank:index')
def add_fine(request):

    if request.method == "POST":

        form = FineTransForm(request.POST)
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
        return render(request, 'bank/add_trans/trans_add_fine.html', {'form': form})


    else:

        form = FineTransForm()
        return render(request, 'bank/add_trans/trans_add_fine.html', {'form': form})

@permission_required('bank.add_transaction',login_url='bank:index')
def add_lab(request):


    if request.method == "POST":

        form = LabTransForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            recipient = form.cleaned_data['recipient'].user
            description = form.cleaned_data['description']
            creator = request.user

            type = TransactionType.objects.get(name='lab')
            status = TransactionStatus.objects.get(name='PR')

            new_trans = Transaction.create_trans(recipient=recipient, value=value, creator=creator,
                                                 description=description,
                                                 type=type, status=status)

            return render(request, 'bank/add_trans/trans_add_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/add_trans/trans_add_lab.html', {'form': form})


    else:

        form = LabTransForm()
        return render(request, 'bank/add_trans/trans_add_lab.html', {'form': form})

@permission_required('bank.add_p2p_transaction',login_url='bank:index')
def add_p2p(request):

    if request.method == "POST":

        form = P2PTransForm(int(request.user.account.balance - hf.p2p_buf), request.POST)
        #form.fields['value'].max_value = int((request.user.account.balance * hf.p2p_proc))
        #print form.fields['value']


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

@login_required()
def dec_trans(request, trans_id):
    print 'decline page'



    trans = Transaction.objects.get(pk=trans_id)
    if trans.creator != request.user and not request.user.has_perm('del_foreign_trans'):
        return redirect(reverse('bank:index'))

    return render(request, 'bank/dec_trans/trans_dec_confirm.html', {'t': trans})

@login_required
def dec_trans_ok(request, trans_id):

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name
    trans = Transaction.objects.get(pk=trans_id)
    if trans.creator != request.user and not request.user.has_perm('del_foreign_trans'):
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        print'decline of trans happening'
        trans.cancel()

        if request.user.has_perm('del_foreign_trans') and trans.creator != request.user:

            trans.status = TransactionStatus.objects.get(name='DA')

        else:
            trans.status = TransactionStatus.objects.get(name='DC')

        trans.save()



    else:
        return redirect(reverse('bank:index'))

    return render(request, 'bank/dec_trans/trans_dec_ok.html', {'transactions': [trans]})

@permission_required('bank.view_pio_trans_list',login_url='bank:index')
def trans_list(request, username):

    user_group_name = User.objects.get(username=username).groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    if user_group_name != 'pioner' and not request.user.has_perm('bank.view_ped_trans_list'):
        return redirect(reverse('bank:index'))

    t_user = User.objects.get(username=username)

    in_trans = Transaction.objects.filter(recipient=t_user).order_by('-creation_date')
    out_trans = Transaction.objects.filter(creator=t_user).order_by('-creation_date')

    return render(request, 'bank/transaction_lists/admin_trans_list.html',
                  {'in_trans': in_trans, 'out_trans': out_trans, 'user_group': user_group_name, 'user': t_user})

@permission_required('bank.manage_trans',login_url='bank:index')
def manage_p2p(request):

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

@permission_required('bank.see_super_table',login_url='bank:index')
def super_table(request):
    table = TransTable(Transaction.objects.all(),order_by='-creation_date')
    RequestConfig(request).configure(table)
    return render(request, 'bank/s_table.html', {'trans': table})



