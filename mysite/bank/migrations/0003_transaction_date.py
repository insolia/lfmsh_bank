# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_auto_20160615_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 17, 16, 31, 1, 417903, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
