# -*- coding: utf-8 -*-
import random
import string
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .tasks import scrape_data

# Create your models here.


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
    url_id = models.SlugField(max_length=6, default=generate_url_id)
    long_url = models.URLField(max_length=200)
    author = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    hits = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    monetize = models.BooleanField(default=True)

    def __unicode__(self):
        return self.url_id

    def get_absolute_url(self):
        return reverse('visiturl', kwargs={"url_id": self.url_id})

    def get_meta_content(self):
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
    system = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    referer = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return str(self.date)


class Token(models.Model):
    user = models.ForeignKey(User)
    uuid = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username
