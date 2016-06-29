from django.shortcuts import render
from django.http import HttpResponse
from bank.models import Account, Transaction
from django.template import Context, loader
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import logout_then_login
from django.views import generic
from django.core.urlresolvers import reverse
from .forms import TransactionForm
from django.utils import timezone



# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    return render(request, 'bank/index.html', {'user_group': user_group_name})


def show_accounts(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (
            settings.LOGIN_URL, request.path))  # reverse('%s?next=%s' % (settings.LOGIN_URL, request.path))

    accounts = Account.objects.order_by('-balance')
    template = loader.get_template('bank/show_all.html')
    context = Context({
        'accounts': accounts,
    })

    return HttpResponse(template.render(context))


class AccsView(generic.ListView):
    template_name = 'bank/show_all.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.order_by('-balance')


def show_my_trans(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    in_trans = Transaction.objects.filter(recipient=request.user).order_by('-last_modified_date')
    out_trans = Transaction.objects.filter(creator=request.user).order_by('-last_modified_date')
    user_group_name = request.user.groups.filter(name__in=['pioner', 'pedsostav', 'admin'])[0].name

    return render(request, 'bank/trans_list.html',
                  {'in_trans': in_trans, 'out_trans': out_trans, 'user_group': user_group_name})


def single_trans(request):
    user_group = request.user.groups.all()

    if user_group:
        user_group = user_group[0]
    else:
        return HttpResponse('no group')

    if user_group.name == 'pioners':
        return redirect(reverse('bank:index'))

    if request.method == "POST":

        form = TransactionForm(request.POST)
        if form.is_valid():
            new_trans = form.save(commit=False)
            new_trans.pub_date = timezone.now()

            user_account = Account.objects.get(user=new_trans.recipient.user)
            print user_account
            # print(new_trans.recipient)
            # print(new_trans.recipient.balance)
            print user_account.balance

            user_account.balance += new_trans.value
            user_account.save()
            new_trans.creator = request.user
            new_trans.save()

            #print(new_trans.recipient.balance)
            print user_account.balance

            new_trans.recipient.balance += new_trans.value

            return render(request, 'bank/trans_ok.html', {'transactions': [new_trans]})
        return render(request, 'bank/trans_add.html', {'form': form})


    else:

        form = TransactionForm()
        return render(request, 'bank/trans_add.html', {'form': form})


def multi_trans(request):
    user_group = request.user.groups.all()

    if user_group:
        user_group = user_group[0]
    else:
        return HttpResponse('no group')

    if user_group.name == 'pioners':
        return redirect(reverse('bank:index'))

    if request.method == "POST":


        print
        print request.POST
        print request.POST['pioner_value']

        new_transactions = []

        for a in Account.objects.all():
            if a.user.username + '_check' in request.POST:
                recipient = a
                value = (request.POST[a.user.username + '_value'])
                if value:
                    value = int(value)
                else:

                    value = 0
                desc = request.POST['description']
                trans = Transaction(recipient=recipient, value=value, description=desc)
                trans.creator = request.user

                trans.save()
                a.balance += value
                a.save()
                new_transactions.append(trans)
        if new_transactions:
            return render(request, 'bank/trans_ok.html', {'transactions': new_transactions})

        else:
            accounts = Account.objects.order_by('user')
            return render(request, 'bank/trans_multi_add.html', {'request': request, 'accounts': accounts})
    else:

        accounts = Account.objects.order_by('user')
        return render(request, 'bank/trans_multi_add.html', {'request': request, 'accounts': accounts})

