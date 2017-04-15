from django import forms
from crispy_forms.bootstrap import StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit

from .models import PageURL, Campaign


class PageURLForm(forms.ModelForm):
    # campaign = forms.IntegerField(required=False)
    class Meta:
        model = PageURL
        fields = ['long_url']

    def __init__(self, *args, **kwargs):
        super(PageURLForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.form_class = 'form-inline'
        # self.helper.field_class = ''
        self.fields['campaign'].widget = forms.HiddenInput()
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            'long_url',
            ButtonHolder(
                Submit('submit', 'Shorten', css_class="btn-primary")
            )

            #FieldWithButtons('long_url', Submit('submit', 'Ujeb', css_class="btn-primary"))
        )


class SimplePageURLForm(forms.ModelForm):
    class Meta:
        model = PageURL
        fields = ['long_url', 'url_id', 'campaign']

    def __init__(self, *args, **kwargs):
        super(SimplePageURLForm, self).__init__(*args, **kwargs)
        self.fields['campaign'].widget = forms.HiddenInput()
        self.fields['campaign'].required = False
        # self.helper.field_class = ''

class ContactForm(forms.Form):
    CHOICES = (
        ('GENERAL', 'General Enquiry'),
        ('SUPPORT', 'Tecnical Support'),
        ('BUSINESS', 'Business Offers')
    )
    from_email = forms.EmailField(label='Your email', required=True)
    subject = forms.ChoiceField(choices=CHOICES)
    message = forms.CharField(widget=forms.Textarea)


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description']

