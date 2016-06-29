# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0011_auto_20160628_0214'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trans_type',
            new_name='TransactionType',
        ),
        migrations.AlterField(
            model_name='account',
            name='otr',
            field=models.CharField(default=b'FI', max_length=2,
                                   choices=[(b'FI', b'First'), (b'SE', b'Second'), (b'TH', b'Third'),
                                            (b'FO', b'Fourth'), (b'PD', b'Ped')]),
        ),
    ]
