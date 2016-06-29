# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recepient',
            field=models.ForeignKey(to='bank.Account'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
