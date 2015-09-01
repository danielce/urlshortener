import json
import random
import string
from django.contrib import messages
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.views.generic import DeleteView, ListView, TemplateView
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from .forms import ContactForm, PageURLForm
from .models import PageURL, Ad, Visit
from .utils import generate_url_id, scrape_data

# Create your views here.


def shorten(request):
    form = PageURLForm(request.POST or None)
    trends = PageURL.objects.all().order_by('-hits')[:5]
    newest = PageURL.objects.all().order_by('-created')[:5]
    context = {'form': form, "trends": trends, "newest": newest}
    if form.is_valid():
        long_url = form.cleaned_data['long_url']
        try:
            shorted = PageURL.objects.get(long_url=long_url)
        except:
            instance = form.save(commit=False)
            url_id = generate_url_id()
            instance.url_id = url_id
            meta = scrape_data(long_url)
            instance.title = meta['title']
            instance.description = meta['description']
            if request.user.is_authenticated():
                instance.author = request.user
            instance.save()
            long_url = instance.long_url
            context.update({"url_id": url_id, "long_url": long_url})
            return render(request, 'home.html', context)
        context.update({"url_id": shorted.url_id, "long_url": shorted.long_url})
    return render(request, 'home.html', context)

def visiturl(request, url_id):
    url = get_object_or_404(PageURL, url_id=url_id)
    url.hits += 1
    url.save()
    visit = Visit()
    visit.url = url
    visit.ip = request.META.get('REMOTE_ADDR')
    visit.user_agent = request.META.get('HTTP_USER_AGENT')
    visit.referer = request.META.get('HTTP_REFERER')
    visit.save()
    if url.monetize == True:
        random_ad = Ad.objects.order_by('?').first()
        context = {"long_url": url.long_url, "random_ad": random_ad}
        return render(request, 'doorway.html', context)
    else:
        return HttpResponseRedirect(url.long_url)


def stat(request, url_id):
    url = PageURL.objects.get(url_id=url_id)
    last_visits = Visit.objects.filter(url=url).order_by('-date')[:10]
    days = Visit.objects.filter(url=url).extra(select={'day': 'date( date )'}).values('day').annotate(clicks=Count('date'))
    day_list = [item['day'] for item in days]
    click_list = [item['clicks'] for item in days]
    lst = {"days":day_list, "clicks":click_list}
    serialized_data = json.dumps(lst)
    if request.is_ajax():
        return HttpResponse(serialized_data, content_type="application/json")
    context = {"url": url, "days": days, "day_list": day_list, "last_visits": last_visits}
    return render(request, 'stat.html', context)

class AboutView(TemplateView):
    template_name = "about.html"


def contact(request):
    form = ContactForm()
    context = {"form": form}
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['d.cichowski@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Oooops! Invalid header found :(')
        messages.success(request, "Your message has been sent!")
        return render(request, 'contact.html', context)
    return render(request, 'contact.html', context)


# def dashboard(request):
#     user = request.user
#     urls = PageURL.objects.filter(author=request.user)
#     context = {'urls': urls}
#     return render(request, 'dashboard.html', context)

class PageURLListView(ListView):
    template_name = 'dashboard.html'
    paginate_by = 20
    context_object_name = 'urls'

    def get_queryset(self):
        return PageURL.objects.filter(author=self.request.user)


def delete_url(request, url_id):
    user = request.user
    if user.is_authenticated:
        obj = PageURL.objects.get(url_id=url_id, author=user)
        if obj != None:
            obj.delete()
            return HttpResponseRedirect(reverse('dashboard'))

