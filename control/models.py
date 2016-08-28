from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class Configuration(models.Model):
    name = models.CharField(max_length=255, default='URLShortner')
    slogan = models.CharField(
        max_length=255,
        default='Simple url shortening service'
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='uploads/')
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    googleplus = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
