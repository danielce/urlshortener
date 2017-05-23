# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from braces.views import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, UpdateView
from shortener.models import Campaign, PageURL
from .forms import (
    TestSuiteForm, BalancedRedirectionForm, FirstTimeRedirectionForm,
    DateRangeRedirectionForm
)
from .models import BalancedRedirection
# Create your views here.


class TestSuiteListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = 'tests_list.html'
    paginate_by = 20
    context_object_name = 'tests'

    def get_queryset(self):
        return Campaign.objects.filter(
            owner=self.request.user,
            campaign_type=Campaign.TESTSUITE,
        ).order_by('-hits')


class TestSuiteCreateView(LoginRequiredMixin, CreateView):
    form_class = TestSuiteForm
    model = Campaign
    template_name = 'testsuite_create.html'

    def get_success_url(self):
        return reverse('test-list')

    def form_valid(self, form):
        super(TestSuiteCreateView, self).form_valid(form)
        self.object.owner = self.request.user
        self.object.campaign_type = Campaign.TESTSUITE
        self.object.save()
        return redirect('test-list')


class TestSuiteUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TestSuiteForm
    model = Campaign
    template_name = 'testsuite_create.html'

    def get_success_url(self):
        return reverse('test-list')


class TestSuiteDetailView(LoginRequiredMixin, ListView):
    context_object_name = 'tests'
    template_name = 'testsuite_detail.html'
    model = Campaign

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return PageURL.objects.filter(
            campaign__pk=pk,
            campaign__campaign_type=Campaign.TESTSUITE
        ).order_by('-created')

    def get_context_data(self, *args, **kwargs):
        context = super(TestSuiteDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['obj'] = Campaign.objects.get(pk=pk)
        return context


class BalancedRedirectionCreateView(LoginRequiredMixin, CreateView):
    form_class = BalancedRedirectionForm
    model = BalancedRedirection
    template_name = 'balanced_create.html'

    def get_success_url(self):
        return reverse('test-list')

    def form_valid(self, form, *args, **kwargs):
        super(BalancedRedirectionCreateView, self).form_valid(form)
        campagin_id = self.kwargs['pk']
        campaign = Campaign.objects.get(pk=campagin_id)

        self.object.owner = self.request.user
        self.object.campaign_type = Campaign.TESTSUITE
        self.object.save()
        PageURL.objects.create(
            campaign=campaign,
            content_object=self.object
        )
        return redirect('test-list')
