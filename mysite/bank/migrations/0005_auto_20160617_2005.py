# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_auto_20160617_2003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='date',
            new_name='last_modified_date',
        ),
    ]
