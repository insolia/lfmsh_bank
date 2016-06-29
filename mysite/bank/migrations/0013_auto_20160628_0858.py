# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0012_auto_20160628_0227'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='counted',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='group1',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='group2',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
