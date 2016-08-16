# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0007_auto_20150827_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageurl',
            name='author',
        ),
    ]
