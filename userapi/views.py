# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView
from .models import Token
# Create your views here.


class TokenListView(ListView):
    template_name = 'tokens.html'
    queryset = Token.objects.all()
    context_object_name = 'tokens'

    def get_queryset(self):
        user = self.request.user
        qs = Token.objects.filter(user=user)
        return qs
