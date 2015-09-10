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
from shortener.views import AboutView, ContactFormView, PageURLListView


urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^contact/$', 'shortener.views.contact', name="contact"),
    url(r'^contact/$', ContactFormView.as_view(), name="contact"),
    url(r'^dashboard/$', PageURLListView.as_view(), name="dashboard"),
    url(r'^$', 'shortener.views.shorten', name="home" ),
    url(r'^(?P<url_id>\w+)/stat$', 'shortener.views.stat', name="stat"),
    url(r'^(?P<url_id>\w+)/delete$', 'shortener.views.delete_url', name="delete_url"),
    url(r'^(?P<url_id>\w+)/$', 'shortener.views.visiturl', name="visiturl"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

