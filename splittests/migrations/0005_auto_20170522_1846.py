# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-22 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('splittests', '0004_auto_20170520_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='daterangeredirection',
            old_name='inactvive_url',
            new_name='inactive_url',
        ),
    ]