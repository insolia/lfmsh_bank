# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank', '0007_transaction_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fac_passed',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='grade',
            field=models.IntegerField(default=8, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='lab_passed',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='otr',
            field=models.CharField(default=b'FI', max_length=2,
                                   choices=[(b'FI', b'First'), (b'SE', b'Second'), (b'TH', b'Third'),
                                            (b'FO', b'Fourth'), (b'PD', b'Not pioner')]),
        ),
        migrations.AddField(
            model_name='account',
            name='sem_attend',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='third_name',
            field=models.CharField(default=b'Not stated', max_length=40),
        ),
        migrations.AddField(
            model_name='transaction',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='modifier',
            field=models.ForeignKey(related_name='modified_trans', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(default=b'AD', max_length=2,
                                   choices=[(b'AD', b'Added'), (b'CO', b'Confirmed'), (b'PR', b'Processed'),
                                            (b'DC', b'Creator declined'), (b'DA', b'Admin declined')]),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(default=b'ELSE', max_length=4, choices=[(b'STEV', b'Every day studies'), (
            b'STSI', ((b'OLYM', b'Olympiad'), (b'EXAM', b'Exam'))), (b'CULT', b'Culture activity'),
                                                                           (b'PENA', b'Penalty'), (b'ELSE', b'Else')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(related_name='created_trans', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(related_name='received_trans', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
