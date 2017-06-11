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
    MobileCreateView,
    MobileUpdateView,
    MaxClickCreateView,
    MaxClickUpdateView,
)


urlpatterns = [
    url(r'^$', TestSuiteListView.as_view(), name="test-list"),
    url(r'^create/$', TestSuiteCreateView.as_view(), name="testsuite-create"),
    url(r'^(?P<pk>\d+)/edit/$', TestSuiteUpdateView.as_view(), name="testsuite-edit"),
    url(r'^(?P<pk>\d+)/balanced$', BalancedRedirectionCreateView.as_view(), name="balanced-create"),
    url(r'^(?P<pk>\d+)/firsttime$', FirstTimeCreateView.as_view(), name="firsttime-create"),
    url(r'^(?P<pk>\d+)/daterange$', DateRangeCreateView.as_view(), name="daterange-create"),
    url(r'^(?P<pk>\d+)/mobile$', MobileCreateView.as_view(), name="mobile-create"),
    url(r'^(?P<pk>\d+)/maxclick$', MaxClickCreateView.as_view(), name="maxclick-create"),
    url(r'^(?P<pk>\d+)/firsttime/(?P<r_id>\d+)/$', FirstTimeUpdateView.as_view(), name="firsttime-edit"),
    url(r'^(?P<pk>\d+)/balanced/(?P<b_id>\d+)/$', BalancedRedirectionUpdateView.as_view(), name="balanced-edit"),
    url(r'^(?P<pk>\d+)/daterange/(?P<r_id>\d+)/$', DateRangeUpdateView.as_view(), name="daterange-edit"),
    url(r'^(?P<pk>\d+)/mobile/(?P<r_id>\d+)/$', MobileUpdateView.as_view(), name="mobile-edit"),
    url(r'^(?P<pk>\d+)/maxclick/(?P<r_id>\d+)/$', MaxClickUpdateView.as_view(), name="maxclick-edit"),
    url(r'^(?P<pk>\d+)/$', TestSuiteDetailView.as_view(), name="testsuite-detail"),
]
