from django.conf.urls import url

from .views import (
    TestSuiteListView, TestSuiteCreateView,
    TestSuiteUpdateView, TestSuiteDetailView,
    BalancedRedirectionCreateView,
    BalancedRedirectionUpdateView,
    FirstTimeCreateView,
    FirstTimeUpdateView,
    DateRangeCreateView,
    DateRangeUpdateView,
)


urlpatterns = [
    url(r'^$', TestSuiteListView.as_view(), name="test-list"),
    url(r'^create/$', TestSuiteCreateView.as_view(), name="testsuite-create"),
    url(r'^(?P<pk>\d+)/edit/$', TestSuiteUpdateView.as_view(), name="testsuite-edit"),
    url(r'^(?P<pk>\d+)/balanced$', BalancedRedirectionCreateView.as_view(), name="balanced-create"),
    url(r'^(?P<pk>\d+)/firsttime$', FirstTimeCreateView.as_view(), name="firsttime-create"),
    url(r'^(?P<pk>\d+)/daterange$', DateRangeCreateView.as_view(), name="daterange-create"),
    url(r'^(?P<pk>\d+)/firsttime/(?P<r_id>\d+)/$', FirstTimeUpdateView.as_view(), name="firsttime-edit"),
    url(r'^(?P<pk>\d+)/balanced/(?P<b_id>\d+)/$', BalancedRedirectionUpdateView.as_view(), name="balanced-edit"),
    url(r'^(?P<pk>\d+)/daterange/(?P<r_id>\d+)/$', DateRangeUpdateView.as_view(), name="daterange-edit"),
    url(r'^(?P<pk>\d+)/$', TestSuiteDetailView.as_view(), name="testsuite-detail"),
]
