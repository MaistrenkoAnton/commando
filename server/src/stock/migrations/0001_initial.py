# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 07:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('discount', models.IntegerField()),
                ('start', models.DateField(default=datetime.datetime(2016, 3, 1, 7, 56, 3, 98818, tzinfo=utc))),
                ('finish', models.DateField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store')),
            ],
            options={
                'ordering': ['title'],
                'db_table': 'stocks',
                'verbose_name': 'stock',
                'verbose_name_plural': 'stocks',
            },
        ),
    ]
