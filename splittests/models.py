# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
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

    def get_edit_url(self):
        return reverse(
            'balanced-edit',
            kwargs={
                'pk': self.short_url.all()[0].campaign.pk,
                'b_id': self.pk,
            }
        )


class FirstTimeRedirection(models.Model):
    first_url = models.URLField(max_length=255)
    long_url = models.URLField(max_length=255)
    pageurl = GenericRelation(PageURL, related_query_name='firsttime')

    def __unicode__(self):
        return self.name

    def dispatch(self, visit, *args, **kwargs):
        pageurl = self.pageurl.all()[0]
        gid = kwargs.get('gid', None)
        if not gid:
            return self.first_url

        visits = Visit.objects.filter(
            url=pageurl, session=gid).count()
        if visits < 2:
            return self.first_url

        return self.long_url

    def get_edit_url(self):
        return reverse(
            'firsttime-edit',
            kwargs={
                'pk': self.pageurl.all()[0].campaign.pk,
                'r_id': self.pk,
            }
        )


class DateRangeRedirection(models.Model):
    active_url = models.URLField(max_length=255)
    inactive_url = models.URLField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pageurl = GenericRelation(PageURL, related_query_name='daterange')

    def __unicode__(self):
        return "DateRange {}".format(self.active_url)

    def dispatch(self, visit, *args, **kwargs):
        now = timezone.now()
        if (self.start < now) and (now < self.end):
            return self.active_url

        return self.inactive_url

    def get_edit_url(self):
        return reverse(
            'daterange-edit',
            kwargs={
                'pk': self.pageurl.all()[0].campaign.pk,
                'r_id': self.pk,
            }
        )


class MobileRedirection(models.Model):
    mobile_url = models.URLField(max_length=255)
    standard_url = models.URLField(max_length=255)
    pageurl = GenericRelation(PageURL, related_query_name='mobile')

    def __unicode__(self):
        return "Mobile {}".format(self.mobile_url)

    def dispatch(self, visit, *args, **kwargs):
        if visit.is_mobile:
            return self.mobile_url

        return self.standard_url

    def get_edit_url(self):
        return reverse(
            'mobile-edit',
            kwargs={
                'pk': self.pageurl.all()[0].campaign.pk,
                'r_id': self.pk
            }
        )


class MaxClickRedirection(models.Model):
    exceed_url = models.URLField(max_length=255)
    standard_url = models.URLField(max_length=255)
    limit = models.PositiveIntegerField(default=1)
    pageurl = GenericRelation(PageURL, related_query_name='maxclick')

    def __unicode__(self):
        return "MaxClick {}".format(self.standard_url)

    def dispatch(self, visit, *args, **kwargs):
        pageurl = self.pageurl.all()[0]
        gid = kwargs.get('gid', None)
        if not gid:
            return self.standard_url

        visits = Visit.objects.filter(
            url=pageurl, session=gid).count()
        if visits > self.limit:
            return self.exceed_url

        return self.standard_url

    def get_edit_url(self):
        return reverse(
            'maxclick-edit',
            kwargs={
                'pk': self.pageurl.all()[0].campaign.pk,
                'r_id': self.pk
            }
        )
