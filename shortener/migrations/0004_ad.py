# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_pageurl_monetize'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('aff_url', models.URLField(unique=True)),
                ('image', models.URLField()),
                ('hits', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
