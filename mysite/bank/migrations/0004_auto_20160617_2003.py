# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(max_length=400),
        ),
    ]
