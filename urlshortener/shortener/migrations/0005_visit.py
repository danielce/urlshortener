# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0004_ad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField(null=True, blank=True)),
                ('user_agent', models.CharField(max_length=200, null=True, blank=True)),
                ('referer', models.CharField(max_length=200, null=True, blank=True)),
                ('url', models.ForeignKey(to='shortener.PageURL')),
            ],
        ),
    ]
