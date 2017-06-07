from django import forms
from django.utils.translation import gettext_lazy as _
from shortener.models import Campaign
from .models import (
    BalancedRedirection, FirstTimeRedirection,
    DateRangeRedirection, MobileRedirection,
    MaxClickRedirection
)


class TestSuiteForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description']


class BalancedRedirectionForm(forms.ModelForm):
    class Meta:
        model = BalancedRedirection
        fields = ['a_rule', 'a_url', 'b_rule', 'b_url']
        labels = {
            'a_rule': _('1st URL weight'),
            'b_rule': _('2nd URL wieght'),
            'a_url': _('first URL'),
            'b_url': _('second URL'),
        }


class FirstTimeRedirectionForm(forms.ModelForm):
    class Meta:
        model = FirstTimeRedirection
        fields = ['first_url', 'long_url']


class DateRangeRedirectionForm(forms.ModelForm):
    class Meta:
        model = DateRangeRedirection
        fields = ['active_url', 'inactive_url', 'start', 'end']


class MobileRedirectionForm(forms.ModelForm):
    class Meta:
        model = MobileRedirection
        fields = ['mobile_url', 'standard_url']


class MaxClickRedirectionForm(forms.ModelForm):
    class Meta:
        model = MaxClickRedirection
        fields = ['standard_url', 'limit', 'exceed_url']
