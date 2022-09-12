from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50
                           , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Full Name')}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}))
    message = forms.CharField(max_length=600,widget=forms.Textarea(
                                  attrs={'rows': 5, 'class': 'form-control', 'placeholder': _('Message')}))

    def send_email(self):
        message = f"From: {self.cleaned_data['name']}\n{self.cleaned_data['message']}"
        send_mail(
            _('User comments'),
            message,
            self.cleaned_data['email'],
            ['discord.1843@gmail.com'],
            fail_silently=True,
        )
