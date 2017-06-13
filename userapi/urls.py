from django.conf.urls import url

from .views import TokenListView
from .api import (
    PageURLListAPIView, PageURLCreateAPIView,
    PageURLDetailAPIView, SimpleRedirectionExpandAPIView,
    CampaignCreateView
)

urlpatterns = [
    url(r'^$', TokenListView.as_view(), name="tokenlist"),
    url(r'^v1/$', PageURLListAPIView.as_view(), name="api-urllist"),
    url(r'^v1/shorten/$', PageURLCreateAPIView.as_view(), name="api-create"),
    url(r'^v1/campaign/$', CampaignCreateView.as_view(), name="api-campaign-create"),
    url(r'^v1/info/(?P<url_id>\w+)/$', PageURLDetailAPIView.as_view(), name="api-detail"),
    url(r'^v1/expand/(?P<url_id>.*)/$', SimpleRedirectionExpandAPIView.as_view(), name="api-expand"),
]
