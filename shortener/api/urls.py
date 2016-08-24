from django.conf.urls import url

from .views import PageURLListAPIView, PageURLCreateAPIView


urlpatterns = [
    url(r'^$', PageURLListAPIView.as_view(), name="api-urllist"),
    url(r'^create/$', PageURLCreateAPIView.as_view(), name="api-create"),
]