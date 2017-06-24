"""urlshortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from shortener.views import (
    AboutView,
    ContactFormView,
    PageURLListView,
    DashboardView,
    ShortenView,
    NewURLFormView,
    UpdateURLFormView,
    StatView,
    delete_url,
    visiturl,
    CampaignListView,
    CampaignCreateView,
    CampaignUpdateView,
    CampaignDetailView,
    NewCampaignURLFormView,
    BulkCampaignCreateView,
    PixelListView, PixelCreateView   
)

urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax/', include('shortener.api.urls')),
    url(r'^contact/$', ContactFormView.as_view(), name="contact"),
    url(r'^control/', include('control.urls')),
    url(r'^settings/', include('core.urls')),
    url(r'^tests/', include('splittests.urls')),
    url(r'^campaigns/$', CampaignListView.as_view(), name="campaigns"),
    url(r'^campaigns/new/$', CampaignCreateView.as_view(), name="campaign-create"),
    url(r'^campaigns/bulk/$', BulkCampaignCreateView.as_view(), name="campaign-bulk"),
    url(r'^campaigns/(?P<pk>\d+)/edit/$',
        CampaignUpdateView.as_view(), name="campaign-update"),
    url(r'^campaigns/(?P<pk>\d+)/$',
        CampaignDetailView.as_view(), name="campaign-detail"),
    url(r'^campaigns/(?P<pk>\d+)/newurl$',
        NewCampaignURLFormView.as_view(), name="campaign-url"),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    url(r'^api/', include('userapi.urls')),
    url(r'^list/$', PageURLListView.as_view(), name="urllist"),
    url(r'^pixels/$', PixelListView.as_view(), name="pixels"),
    url(r'^pixels/create/$', PixelCreateView.as_view(), name="pixels_create"),
    url(r'^new/$', NewURLFormView.as_view(), name="newurl"),
    url(r'^$', ShortenView.as_view(), name="home"),
    url(r'^(?P<url_id>\w+)/stat$', StatView.as_view(), name="stat"),
    url(r'^(?P<url_id>\w+)/edit$', UpdateURLFormView.as_view(), name="editurl"),
    url(r'^(?P<url_id>\w+)/delete$', delete_url, name="delete_url"),
    url(r'^(?P<url_id>\w+)/$', visiturl, name="visiturl"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
