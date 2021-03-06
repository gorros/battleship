# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 11:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='status',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Finished')], default=0),
        ),
        migrations.AlterField(
            model_name='battle',
            name='turn',
            field=models.IntegerField(choices=[(0, 'Computer'), (1, 'Player')], default=1),
        ),
        migrations.AlterField(
            model_name='ship',
            name='category',
            field=models.IntegerField(choices=[(5, 'Aircraft container'), (4, 'Battle ship'), (3, 'Cruiser'), (2, 'Destroyer'), (1, 'Submarine')]),
        ),
        migrations.AlterField(
            model_name='ship',
            name='health',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
