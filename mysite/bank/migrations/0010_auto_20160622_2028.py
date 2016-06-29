# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0009_auto_20160622_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='last_modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='modifier',
            field=models.ForeignKey(related_name='modified_trans', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(default=b'ELSE', max_length=4,
                                   choices=[(b'a', b'c'), (b'b', b'd'), (b'ELSE', b'Else')]),
        ),
    ]
