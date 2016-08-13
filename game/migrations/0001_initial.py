# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 11:11
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('player_board', jsonfield.fields.JSONField(default={})),
                ('computer_board', jsonfield.fields.JSONField(default={'(1,1)': 0, '(1,10)': 0, '(1,2)': 0, '(1,3)': 0, '(1,4)': 0, '(1,5)': 0, '(1,6)': 0, '(1,7)': 0, '(1,8)': 0, '(1,9)': 0, '(10,1)': 0, '(10,10)': 0, '(10,2)': 0, '(10,3)': 0, '(10,4)': 0, '(10,5)': 0, '(10,6)': 0, '(10,7)': 0, '(10,8)': 0, '(10,9)': 0, '(2,1)': 0, '(2,10)': 0, '(2,2)': 0, '(2,3)': 0, '(2,4)': 0, '(2,5)': 0, '(2,6)': 0, '(2,7)': 0, '(2,8)': 0, '(2,9)': 0, '(3,1)': 0, '(3,10)': 0, '(3,2)': 0, '(3,3)': 0, '(3,4)': 0, '(3,5)': 0, '(3,6)': 0, '(3,7)': 0, '(3,8)': 0, '(3,9)': 0, '(4,1)': 0, '(4,10)': 0, '(4,2)': 0, '(4,3)': 0, '(4,4)': 0, '(4,5)': 0, '(4,6)': 0, '(4,7)': 0, '(4,8)': 0, '(4,9)': 0, '(5,1)': 0, '(5,10)': 0, '(5,2)': 0, '(5,3)': 0, '(5,4)': 0, '(5,5)': 0, '(5,6)': 0, '(5,7)': 0, '(5,8)': 0, '(5,9)': 0, '(6,1)': 0, '(6,10)': 0, '(6,2)': 0, '(6,3)': 0, '(6,4)': 0, '(6,5)': 0, '(6,6)': 0, '(6,7)': 0, '(6,8)': 0, '(6,9)': 0, '(7,1)': 0, '(7,10)': 0, '(7,2)': 0, '(7,3)': 0, '(7,4)': 0, '(7,5)': 0, '(7,6)': 0, '(7,7)': 0, '(7,8)': 0, '(7,9)': 0, '(8,1)': 0, '(8,10)': 0, '(8,2)': 0, '(8,3)': 0, '(8,4)': 0, '(8,5)': 0, '(8,6)': 0, '(8,7)': 0, '(8,8)': 0, '(8,9)': 0, '(9,1)': 0, '(9,10)': 0, '(9,2)': 0, '(9,3)': 0, '(9,4)': 0, '(9,5)': 0, '(9,6)': 0, '(9,7)': 0, '(9,8)': 0, '(9,9)': 0})),
                ('turn', models.IntegerField(choices=[(0, 'Computer'), (1, 'Player')], default=1, max_length=1)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Finished')], default=0, max_length=1)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.IntegerField(choices=[(5, 'Aircraft container'), (4, 'Battle ship'), (3, 'Cruiser'), (2, 'Destroyer'), (1, 'Submarine')], max_length=1)),
                ('health', models.IntegerField(max_length=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('coordinates', jsonfield.fields.JSONField(default=[])),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Battle')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
