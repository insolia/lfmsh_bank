from bank.models import *
from django.contrib.auth.models import Group
from bank.helper_functions import daily_tax, get_tax_desc



### execfile('daily_tax.py')

for u in User.objects.filter(groups__name='pioner'):
    creator = User.objects.get(username='admin')
    type = TransactionType.objects.get(name='daily_tax')
    status = TransactionStatus.objects.get(name='PR')
    t = Transaction.create_trans(recipient=u, value=daily_tax, creator=creator, description=get_tax_desc(), type=type,
                                 status=status)

    print t.counted

