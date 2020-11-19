from django import forms


class CreateQRForm(forms.Form):
    url = forms.URLField(label='Destination Website')
