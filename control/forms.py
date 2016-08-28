from django import forms
from crispy_forms.bootstrap import StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit

from .models import Configuration


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['name', 'slogan', 'company_name', 'logo', 'address',
                  'email', 'facebook', 'twitter', 'googleplus', 'youtube']
