import json
from user_agents import parse

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.views.generic import FormView, ListView, TemplateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy

from .forms import ContactForm, PageURLForm
from .models import PageURL, Ad, Visit, Token

# Create your views here.


class ShortenView(FormView):
    form_class = PageURLForm
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super(ShortenView, self).get_context_data(*args, **kwargs)
        url_qs = PageURL.objects.all()
        context['trends'] = url_qs.order_by('-hits')[:5]
        context['newest'] = url_qs.order_by('-created')[:5]

        return context

    def form_valid(self, form, **kwargs):
        long_url = form.cleaned_data['long_url']
        try:
            short = PageURL.objects.get(long_url=long_url)
        except PageURL.DoesNotExist:
            instance = form.save(commit=False)
            if self.request.user.is_authenticated():
                instance.author = self.request.user
            instance.save()
            long_url = instance.long_url

        return super(ShortenView, self).form_valid(form, **kwargs)


class TokenListView(ListView):
    template_name = 'tokens.html'
    queryset = Token.objects.all()
    context_object_name = 'tokens'

    def get_queryset(self):
        user = self.request.user
        qs = Token.objects.filter(user=user)
        return qs


def visiturl(request, url_id):
    url = get_object_or_404(PageURL, url_id=url_id)
    ua = parse(request.META.get('HTTP_USER_AGENT'))
    url.hits += 1
    url.save()
    visit = Visit(
        url=url,
        ip=request.META.get('REMOTE_ADDR'),
        referer=request.META.get('HTTP_REFERER'),
        user_agent=str(ua),
        browser=ua.browser,
        system=ua.os,
        device=ua.device,
    )
    visit.save()
    if url.monetize:
        random_ad = Ad.objects.order_by('?').first()
        context = {"long_url": url.long_url, "random_ad": random_ad}
        return render(request, 'doorway.html', context)
    else:
        return HttpResponseRedirect(url.long_url)


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
            serialized_data = json.dumps(lst)
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


class PageURLListView(ListView):
    template_name = 'dashboard.html'
    paginate_by = 20
    context_object_name = 'urls'

    def get_queryset(self):
        return PageURL.objects.filter(author=self.request.user)


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
