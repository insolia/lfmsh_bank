import django_tables2 as tables
from .models import *

class TransTable(tables.Table):
    class Meta:
        model = Transaction
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue table table-striped'}
        exclude = ('last_modified_date','modifier')

    def render_creation_date(self, value):
        return value.strftime("%d.%m.%Y %H:%M")

    def render_creator(self, value):
        return value.account

    def render_recipient(self, value):
        return value.account