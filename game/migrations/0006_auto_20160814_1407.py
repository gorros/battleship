# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20160813_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.FBUser'),
        ),
    ]