# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 14:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160813_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('by', models.IntegerField(choices=[(0, 'Computer'), (1, 'Player')])),
                ('x', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('y', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='battle',
            name='player_board',
            field=jsonfield.fields.JSONField(default={'(1, 1)': -1, '(1, 10)': -1, '(1, 2)': -1, '(1, 3)': -1, '(1, 4)': -1, '(1, 5)': -1, '(1, 6)': -1, '(1, 7)': -1, '(1, 8)': -1, '(1, 9)': -1, '(10, 1)': -1, '(10, 10)': -1, '(10, 2)': -1, '(10, 3)': -1, '(10, 4)': -1, '(10, 5)': -1, '(10, 6)': -1, '(10, 7)': -1, '(10, 8)': -1, '(10, 9)': -1, '(2, 1)': -1, '(2, 10)': -1, '(2, 2)': -1, '(2, 3)': -1, '(2, 4)': -1, '(2, 5)': -1, '(2, 6)': -1, '(2, 7)': -1, '(2, 8)': -1, '(2, 9)': -1, '(3, 1)': -1, '(3, 10)': -1, '(3, 2)': -1, '(3, 3)': -1, '(3, 4)': -1, '(3, 5)': -1, '(3, 6)': -1, '(3, 7)': -1, '(3, 8)': -1, '(3, 9)': -1, '(4, 1)': -1, '(4, 10)': -1, '(4, 2)': -1, '(4, 3)': -1, '(4, 4)': -1, '(4, 5)': -1, '(4, 6)': -1, '(4, 7)': -1, '(4, 8)': -1, '(4, 9)': -1, '(5, 1)': -1, '(5, 10)': -1, '(5, 2)': -1, '(5, 3)': -1, '(5, 4)': -1, '(5, 5)': -1, '(5, 6)': -1, '(5, 7)': -1, '(5, 8)': -1, '(5, 9)': -1, '(6, 1)': -1, '(6, 10)': -1, '(6, 2)': -1, '(6, 3)': -1, '(6, 4)': -1, '(6, 5)': -1, '(6, 6)': -1, '(6, 7)': -1, '(6, 8)': -1, '(6, 9)': -1, '(7, 1)': -1, '(7, 10)': -1, '(7, 2)': -1, '(7, 3)': -1, '(7, 4)': -1, '(7, 5)': -1, '(7, 6)': -1, '(7, 7)': -1, '(7, 8)': -1, '(7, 9)': -1, '(8, 1)': -1, '(8, 10)': -1, '(8, 2)': -1, '(8, 3)': -1, '(8, 4)': -1, '(8, 5)': -1, '(8, 6)': -1, '(8, 7)': -1, '(8, 8)': -1, '(8, 9)': -1, '(9, 1)': -1, '(9, 10)': -1, '(9, 2)': -1, '(9, 3)': -1, '(9, 4)': -1, '(9, 5)': -1, '(9, 6)': -1, '(9, 7)': -1, '(9, 8)': -1, '(9, 9)': -1}),
        ),
        migrations.AddField(
            model_name='move',
            name='battle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='game.Battle'),
        ),
    ]