from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
from .models import Advert


class AdvertListView(ListView):
	model = Advert
	context_object_name = 'adverts'