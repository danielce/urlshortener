from django.conf.urls import url

from .views import ProfileFormView


urlpatterns = [
    url(r'^$', ProfileFormView.as_view(), name="profile"),
]
