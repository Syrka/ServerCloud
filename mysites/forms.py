from django import forms
from mysites.models import Site


class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['profile', 'url', 'status', 'ssl_cert', 'timeout', 'address', 'ping', 'content_changed',
                  'content_type']
