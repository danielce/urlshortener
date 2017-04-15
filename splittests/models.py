# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from shortner.models import PageURL

# Create your models here.

class BalancedURL(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    name =  models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)