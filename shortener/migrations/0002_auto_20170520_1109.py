# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-20 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageurl',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
