# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import random
import string

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from shortener.models import PageURL, Visit

# Create your models here.
User = settings.AUTH_USER_MODEL


class BalancedRedirection(models.Model):
    a_rule = models.IntegerField()
    b_rule = models.IntegerField()
    a_url = models.URLField(max_length=255)
    b_url = models.URLField(max_length=255)
    a_hits = models.PositiveIntegerField(default=0)
    b_hits = models.PositiveIntegerField(default=0)
    short_url = GenericRelation(PageURL, related_query_name='balanced')

    def __unicode__(self):
        return self.a_url

    def dispatch(self, *args, **kwargs):
        total = self.short_url.all()[0].hits
        if total < 2:
            self.a_hits += 1
            self.save()
            return self.a_url
        d = (self.a_hits / total) * 100
        if d < self.a_rule:
            self.a_hits += 1
            self.save()
            return self.a_url

        self.b_hits += 1
        self.save()
        return self.b_url


class FirstTimeRedirection(models.Model):
    first_url = models.URLField(max_length=255)
    long_url = models.URLField(max_length=255)
    pageurl = GenericRelation(PageURL, related_query_name='firsttime')

    def __unicode__(self):
        return self.name

    def dispatch(self, visit):
        session = visit.session
        visits = Visit.objects.filter(session=session).count()
        if visits < 2:
            return self.first_url

        return self.long_url


class DateRangeRedirection(models.Model):
    active_url = models.URLField(max_length=255)
    inactive_url = models.URLField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pageurl = GenericRelation(PageURL, related_query_name='daterange')

    def __unicode__(self):
        return self.name

    def dispatch(self, visit):
        now = timezone.now()
        if (self.start < now) and (now < self.end):
            return self.active_url

        return self.inactvive_url
