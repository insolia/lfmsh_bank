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
from .trans_form  import TransactionForm
from django.utils import timezone



# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect(('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path)))

    user_group = request.user.groups.all()

    print(user_group)
    print request.user

    if user_group:
        user_group = user_group[0]
    else:
        return HttpResponse('no group')


    print user_group
    print request.user

    if user_group.name == 'pioners':
        return render(request, 'bank/index_pioner.html', {'user': request.user,'request': request})

    if user_group.name == 'pedsostav':
        return render(request, 'bank/index_ped.html', {'user': request.user,'request': request})

def show_accounts(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) #reverse('%s?next=%s' % (settings.LOGIN_URL, request.path))


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
        """Return the last five published questions."""
        return Account.objects.order_by('-balance')

def show_my_account(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    user_account = Account.objects.filter(user = request.user)[0]
    transactions = Transaction.objects.filter(recepient = user_account).order_by('-last_modified_date')
    return render(request, 'bank/pioner_acc.html', {'account': user_account, 'transactions': transactions, 'request':request})




def pay(request):


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


            user_account = Account.objects.get(user=new_trans.recepient.user)
            print user_account
            user_account.balance += new_trans.value
            user_account.save()

            print(new_trans.recepient.balance)
            new_trans.save()

            return render(request, 'bank/trans_ok.html', {'account': user_account,'request': request})
        return render(request, 'bank/trans_add.html', {'form': form})


    else:

        form = TransactionForm()
        return render(request, 'bank/trans_add.html', {'form': form})

