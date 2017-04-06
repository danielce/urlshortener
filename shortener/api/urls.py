from django.conf.urls import url

from .views import (
    CountryAPIView, DeviceAPIView,
    DailyHitsAPIView, BestPerformersAPIView
)

urlpatterns = [
    url(r'^countries/$', CountryAPIView.as_view(), name="api-countries"),
    url(r'^devices/$', DeviceAPIView.as_view(), name="api-devices"),
    url(r'^daily/$', DailyHitsAPIView.as_view(), name="api-daily"),
    url(r'^best-performers/$', BestPerformersAPIView.as_view(),
        name="api-bestperformers"),
]
