from django.conf.urls import url

from .views import TokenListView
from .api import  PageURLListAPIView, PageURLCreateAPIView


urlpatterns = [
    url(r'^$', TokenListView.as_view(), name="token_list"),
    url(r'^api1/$', PageURLListAPIView.as_view(), name="api-urllist"),
    url(r'^api1/create/$', PageURLCreateAPIView.as_view(), name="api-create"),
]
