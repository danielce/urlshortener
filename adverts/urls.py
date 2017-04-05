from django.conf.urls import url

from .views import AdvertListView


urlpatterns = [
    url(r'^$', AdvertListView.as_view(), name="advert_list"),
]
