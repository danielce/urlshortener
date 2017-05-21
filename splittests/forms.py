from django import forms
from shortener.models import Campaign
from .models import (
    BalancedRedirection, FirstTimeRedirection,
    DateRangeRedirection
)


class TestSuiteForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description']


class BalancedRedirectionForm(forms.ModelForm):
    class Meta:
        model = BalancedRedirection
        fields = ['a_rule', 'a_url', 'b_rule', 'b_url']


class FirstTimeRedirectionForm(forms.ModelForm):
    class Meta:
        model = FirstTimeRedirection
        fields = ['first_url', 'long_url']


class DateRangeRedirectionForm(forms.ModelForm):
    class Meta:
        model = DateRangeRedirection
        fields = ['active_url', 'inactive_url', 'start', 'end']
