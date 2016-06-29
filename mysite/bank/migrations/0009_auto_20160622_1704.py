# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0008_auto_20160622_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(related_name='created_trans', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(related_name='received_trans', to=settings.AUTH_USER_MODEL),
        ),
    ]
