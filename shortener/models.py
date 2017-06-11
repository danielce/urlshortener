# -*- coding: utf-8 -*-
import random
import string
import uuid

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

# Create your models here.
User = settings.AUTH_USER_MODEL


class Campaign(models.Model):
    LINKGROUP = 'gr'
    TESTSUITE = 'ts'
    CAMPAIGN_TYPE_CHOICES = (
        (LINKGROUP, _("linkgroup")),
        (TESTSUITE, _("testsuite")),
    )
    owner = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)
    campaign_type = models.CharField(
        max_length=2, choices=CAMPAIGN_TYPE_CHOICES, default=LINKGROUP
    )

    def __unicode__(self):
        return self.name

    @property
    def urls(self):
        return self.pageurl_set.count()


def generate_url_id(length=6):
    sys_random = random.SystemRandom()
    while True:
        url_id = ''.join(
            sys_random.sample(string.ascii_lowercase +
                              string.ascii_uppercase, length)
        )
        try:
            checkurl = PageURL.objects.get(url_id=url_id)
        except PageURL.DoesNotExist:
            return url_id


class PageURL(models.Model):
    SIMPLE = 'simple'
    BALANCED = 'balanced'
    DATE_RANGE = 'daterange'
    FIRST_TIME = 'firsttime'
    MOBILE = 'mobile'
    TYPE_CHOICES = (
        (SIMPLE, _('simple')),
        (BALANCED, _('balanced')),
        (DATE_RANGE, _('daterange')),
        (FIRST_TIME, _('firsttime')),
        (MOBILE, _('mobile'))
    )
    url_id = models.SlugField(max_length=6, default=generate_url_id)
    long_url = models.URLField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    hits = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    monetize = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    campaign = models.ForeignKey(Campaign, blank=True, null=True)
    # url_type = models.CharField(max_length=50, choices=TYPE_CHOICES,
    #                             default=SIMPLE
    #                             )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.url_id

    def get_absolute_url(self):
        return reverse('visiturl', kwargs={"url_id": self.url_id})

    def get_meta_content(self):
        from .tasks import scrape_data
        if not self.long_url:
            return

        data = scrape_data.delay(self.long_url)
        meta = data.get()
        self.title = meta['title']
        self.description = meta['description']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.get_meta_content()

        return super(PageURL, self).save(*args, **kwargs)


class Ad(models.Model):
    title = models.CharField(max_length=255)
    aff_url = models.URLField(unique=True)
    image = models.URLField()
    hits = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title


class Visit(models.Model):
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    url = models.ForeignKey(PageURL)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=200, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    browser_version = models.CharField(max_length=255, null=True, blank=True)
    system = models.CharField(max_length=255, null=True, blank=True)
    system_version = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    referer = models.CharField(max_length=200, null=True, blank=True)
    session = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=True)
    is_tablet = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    is_touch = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.date)


class SimpleRedirection(models.Model):
    long_url = models.URLField(max_length=200)
    short_url = GenericRelation(PageURL, related_query_name='simple')

    def dispatch(self, *args, **kwargs):
        return self.long_url
