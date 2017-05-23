from django.conf.urls import url

from .views import (
    TestSuiteListView, TestSuiteCreateView,
    TestSuiteUpdateView, TestSuiteDetailView,
    BalancedRedirectionCreateView
)


urlpatterns = [
    url(r'^$', TestSuiteListView.as_view(), name="test-list"),
    url(r'^create/$', TestSuiteCreateView.as_view(), name="testsuite-create"),
    url(r'^(?P<pk>\d+)/edit/$', TestSuiteUpdateView.as_view(), name="testsuite-edit"),
    url(r'^(?P<pk>\d+)/balanced$', BalancedRedirectionCreateView.as_view(), name="balanced-create"),
    url(r'^(?P<pk>\d+)/$', TestSuiteDetailView.as_view(), name="testsuite-detail"),
]
