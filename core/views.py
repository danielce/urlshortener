# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.views.generic.edit import UpdateView

from invitations.models import Invitation

from .models import Organization
from .forms import OrganizationForm, InvitationForm

User = get_user_model()


class OrganizationUpdateView(UpdateView):
    form_class = OrganizationForm
    template_name = 'organization_update.html'
    model = Organization

    def get_object(self):
        return self.request.user.organization


class OrganizationUsersListView(ListView):
    model = User
    paginate_by = 20
    template_name = 'users.html'
    context_object_name = 'users'

    def get_queryset(self, *args, **kwargs):
        organization = self.request.user.organization
        if organization:
            return self.model.objects.filter(
                organization=organization
            )
        return []


class InvitationFormView(FormView):
    form_class = InvitationForm
    template_name = 'invitation.html'

    def get_success_url(self):
        return reverse('users-list')

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data['email']
        invite = Invitation.create(email, inviter=request.user)
        invite.send_invitation(request)
        return super(InvitationFormView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        organization = request.user.organization
        if organization and not organization.can_create_user():
            return redirect(reverse('users-list'))

        return super(InvitationFormView, self).dispatch(
            request, *args, **kwargs
        )
