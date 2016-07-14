from django.contrib import admin

# Register your models here.
from bank.models import Account, Transaction, TransactionType, TransactionStatus

admin.site.register(Account)

admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(TransactionStatus)
