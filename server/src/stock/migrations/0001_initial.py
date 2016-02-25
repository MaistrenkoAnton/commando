# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 09:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
                ('description', models.TextField()),
                ('new_price', models.IntegerField()),
                ('end_time', models.DateField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store')),
            ],
        ),
    ]
