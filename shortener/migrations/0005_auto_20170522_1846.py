# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-22 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0004_auto_20170520_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageurl',
            name='long_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
