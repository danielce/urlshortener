from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class PageURL(models.Model):
	url_id = models.SlugField(max_length=6)
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
		return reverse('visiturl', kwargs={"url_id": self.url_id })


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
	referer = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return str(self.date)