# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-05 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='has_profile',
            field=models.BooleanField(default=False),
        ),
    ]
