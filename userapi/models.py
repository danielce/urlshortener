# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Token(models.Model):
    user = models.ForeignKey(User)
    uuid = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.uuid)
