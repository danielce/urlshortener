from django.shortcuts import render
from django.views.generic import UpdateView
# Create your views here.

from .forms import ProfileForm
from .models import Configuration


class ProfileFormView(UpdateView):
    template_name = "profile.html"
    form_class = ProfileForm

    def get_object(self):
        return Configuration.objects.get(pk=1)


# context processor for 
def get_configuration(request):
    context = {}
    obj = Configuration.objects.get(pk=1)
    context['config'] = obj
    return context