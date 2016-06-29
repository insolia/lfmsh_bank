# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0010_auto_20160622_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trans_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('group1', models.CharField(max_length=30, null=True)),
                ('group2', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.ForeignKey(to='bank.Trans_type'),
        ),
    ]
