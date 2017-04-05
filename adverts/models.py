from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Advert(models.Model):
    TEXT = 'TX'
    IMAGE = 'IM'
    VIDEO = 'VI'
    ADVERT_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    )

    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    advert_type = models.CharField(
        max_length=2,
        choices=ADVERT_TYPE_CHOICES,
        default=TEXT,
    )
    image_url = models.URLField()
    hits = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title
