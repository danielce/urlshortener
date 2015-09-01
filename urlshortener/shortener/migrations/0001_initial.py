# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_id', models.SlugField(max_length=6)),
                ('long_url', models.URLField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hits', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
