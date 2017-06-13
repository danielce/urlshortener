import json
import hashlib
from user_agents import parse

from django.contrib import messages
from django.contrib.gis.geoip2 import GeoIP2
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count, Sum, F
from django.views.generic import (
    FormView, ListView, TemplateView, DetailView, CreateView, UpdateView
)
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy

from braces.views import LoginRequiredMixin

from control.models import Configuration
from .forms import (
    ContactForm, PageURLForm, SimplePageURLForm, CampaignForm,
    BulkCampaignForm,
)
from .models import PageURL, Ad, Visit, Campaign
from .tasks import process_bulk

# Create your views here.


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


class ShortenView(TemplateView):
    template_name = 'index.html'
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ShortenView, self).get_context_data(*args, **kwargs)
    #     url_qs = PageURL.objects.all()
    #     context['trends'] = url_qs.order_by('-hits')[:5]
    #     context['newest'] = url_qs.order_by('-created')[:5]

    #     return context

    # def form_valid(self, form, **kwargs):
    #     long_url = form.cleaned_data['long_url']
    #     try:
    #         short = PageURL.objects.get(long_url=long_url)
    #     except PageURL.DoesNotExist:
    #         instance = form.save(commit=False)
    #         if self.request.user.is_authenticated():
    #             instance.author = self.request.user
    #         instance.save()
    #         long_url = instance.long_url

    #     return super(ShortenView, self).form_valid(form, **kwargs)


def visiturl(request, url_id):
    url = get_object_or_404(PageURL, url_id=url_id)
    ua = parse(request.META.get('HTTP_USER_AGENT'))
    url.hits += 1
    url.save()
    g = GeoIP2()
    ip = request.META.get('REMOTE_ADDR')
    ip = '88.80.113.1'
    gid = request.COOKIES.get('gid', None)
    if not gid:
        hsh = "{0}:{1}:{2}:{3}".format(
            ip, ua.browser.version_string,
            ua.os.version_string, ua.device.family
        )
        gid = hashlib.sha256(hsh).hexdigest()
        print gid
    visit = Visit(
        url=url,
        ip=ip,
        referer=request.META.get('HTTP_REFERER'),
        user_agent=str(ua),
        browser=ua.browser.family,
        browser_version=ua.browser.version_string,
        system=ua.os.family,
        system_version=ua.os.version_string,
        device=ua.device.family,
        brand=ua.device.brand,
        model=ua.device.model,
        session=gid,
        is_mobile=ua.is_mobile,
        is_tablet=ua.is_tablet,
        is_pc=ua.is_pc,
        is_bot=ua.is_bot,
        is_touch=ua.is_touch_capable,
    )
    try:
        geo = g.city(ip)
    except:
        pass
    else:
        visit.city = geo['city']
        visit.country = geo['country_name']
        visit.country_code = geo['country_code']
        visit.postal_code = geo['postal_code']
        visit.region = geo['region']
        visit.longitude = geo['longitude']
        visit.latitude = geo['latitude']
    visit.save()
    if url.content_object:
            long_url = url.content_object.dispatch(visit, gid=gid)
    else:
        long_url = url.long_url
    if url.monetize:
        random_ad = Ad.objects.order_by('?').first()
        context = {"long_url": long_url, "random_ad": random_ad}
        return render(request, 'doorway.html', context)
    else:
        response = HttpResponseRedirect(long_url)
        response.set_cookie('gid', gid)
        return response


class StatView(DetailView):
    model = PageURL
    slug_url_kwarg = 'url_id'
    slug_field = 'url_id'
    template_name = 'stat.html'
    context_object_name = 'url'

    def get_context_data(self, **kwargs):
        context = super(StatView, self).get_context_data(**kwargs)
        url = self.object
        context['last_visits'] = Visit.objects.filter(
            url=url).order_by('-date')[:10]
        context['days'] = Visit.objects.filter(url=url).extra(
            select={'day': 'date( date )'}).values('day').annotate(
            clicks=Count('date')
        )
        context['day_list'] = [item['day'] for item in context['days']]
        context['click_list'] = [item['clicks'] for item in context['days']]

        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            lst = {
                "days": context['day_list'],
                "clicks": context['click_list'],
            }
            serialized_data = json.dumps(lst, default=date_handler)
            return HttpResponse(
                serialized_data,
                content_type="application/json",
            )

        return super(StatView, self).get(request, *args, **kwargs)


class AboutView(TemplateView):
    template_name = "about.html"


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        config = Configuration.objects.get(pk=1)
        context['config'] = config
        return context

    def form_valid(self, form):
        from_email = form.cleaned_data['from_email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        try:
            send_mail(subject, message, from_email, ['admin@trashbox.com'])
        except BadHeaderError:
            return HttpResponse('Oooops! Invalid header found :(')
        return super(ContactFormView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Your message has been sent!")
        return reverse('contact')


class PageURLListView(LoginRequiredMixin, ListView):
    template_name = 'urllist.html'
    paginate_by = 20
    context_object_name = 'urls'

    def get_queryset(self):
        return PageURL.objects.filter(
            author=self.request.user
        ).order_by('-hits')


class NewURLFormView(LoginRequiredMixin, FormView):
    form_class = SimplePageURLForm
    template_name = 'new_url.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        items = PageURL.objects.filter(
            author=self.request.user
        ).aggregate(
            hits=Sum(
                F('hits')),
            count=Count(F('id'))
        )
        context['items'] = items
        return context


def delete_url(request, url_id):
    user = request.user
    if user.is_authenticated:
        try:
            obj = PageURL.objects.get(url_id=url_id, author=user)
        except PageURL.DoesNotExist:
            pass
        else:
            obj.delete()

    return HttpResponseRedirect(reverse('dashboard'))


class CampaignListView(LoginRequiredMixin, ListView):
    template_name = 'campaigns.html'
    paginate_by = 20
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(
            owner=self.request.user
        ).order_by('-created')


class CampaignCreateView(LoginRequiredMixin, CreateView):
    form_class = CampaignForm
    model = Campaign
    template_name = 'campaign_create.html'

    def get_success_url(self):
        return reverse('campaigns')

    def form_valid(self, form):
        super(CampaignCreateView, self).form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CampaignForm
    model = Campaign
    template_name = 'campaign_create.html'

    def get_success_url(self):
        return reverse('campaigns')


class CampaignDetailView(LoginRequiredMixin, ListView):
    context_object_name = 'urls'
    template_name = 'campaign_detail.html'
    model = Campaign

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return PageURL.objects.filter(
            campaign__pk=pk
        ).order_by('-created')

    def get_context_data(self, *args, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['obj'] = Campaign.objects.get(pk=pk)
        return context


class NewCampaignURLFormView(LoginRequiredMixin, CreateView):
    form_class = SimplePageURLForm
    template_name = 'new_url.html'
    model = PageURL

    def get_initial(self):
        initial = super(NewCampaignURLFormView, self).get_initial()
        initial['campaign'] = self.kwargs.get('pk')

        return initial

    def get_success_url(self):
        return reverse('campaigns')

    def form_valid(self, form):
        super(NewCampaignURLFormView, self).form_valid(form)
        campaign = Campaign.objects.get(pk=self.kwargs.get('pk'))
        self.object.campaign = campaign
        self.object.author = self.request.user
        self.object.url_type = PageURL.SIMPLE
        self.object.save()
        return redirect(self.get_success_url())


class BulkCampaignCreateView(LoginRequiredMixin, CreateView):
    form_class = BulkCampaignForm
    model = Campaign
    template_name = 'campaign_bulk.html'

    def get_success_url(self):
        return reverse('campaigns')

    def form_valid(self, form):
        super(BulkCampaignCreateView, self).form_valid(form)
        self.object.owner = self.request.user
        self.object.url_type = PageURL.SIMPLE
        self.object.save()
        urls = form.cleaned_data['urls']
        process_bulk.delay(urls, self.object)
        return redirect(self.get_success_url())
