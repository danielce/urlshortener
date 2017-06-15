# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Token
# Create your views here.


class TokenListView(DetailView):
    template_name = 'tokens.html'
    queryset = Token.objects.all()
    context_object_name = 'token'

    def get_object(self):
        user = self.request.user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(
                user=user
            )
        return token
