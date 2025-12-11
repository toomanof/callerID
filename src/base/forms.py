from django import forms


class CallerIDForm(forms.Form):
    phone = forms.CharField(label="Your phone", max_length=100)
