from django import forms

from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address', 'city', 'zipcode', 'phone', 'vat']


class InvitationForm(forms.Form):
    email = forms.EmailField()
