# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class Organization(models.Model):
    FREE = 'fr'
    BASIC = 'bs'
    PRO = 'pr'
    ENTERPRISE = 'nt'
    ACCOUNT_TYPES = (
        (FREE, _('Free')),
        (BASIC, _('Basic')),
        (PRO, _('Pro')),
        (ENTERPRISE, _('Enterprise')),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=2,
        choices=ACCOUNT_TYPES, default=FREE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    vat = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    def __unicode__(self):
        return self.name

    def get_account_limits(self):
        limits = settings.ACCOUNT_TYPE_LIMITS
        acc_type = self.account_type
        return limits[acc_type]

    def can_create_user(self):
        limits = self.get_account_limits()
        limit = limits['users']
        users = User.objects.filter(organization=self).count
        return users < limit


def create_simple_organization():
    return Organization.objects.create(
        account_type=Organization.FREE
    )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    created = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_supervisor = models.BooleanField(_('is_supervisor'), default=False)
    organization = models.ForeignKey(Organization,
        blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
