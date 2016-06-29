# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0005_auto_20160617_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='recepient',
            new_name='recipient',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(max_length=400, blank=True),
        ),
    ]
