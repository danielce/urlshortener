# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Organization, User

# Register your models here.

admin.site.register(Organization)
admin.site.register(User)
