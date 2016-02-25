# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 09:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20160225_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.ForeignKey(blank=True, default=2, on_delete=django.db.models.deletion.CASCADE, to='stock.Stock'),
            preserve_default=False,
        ),
    ]