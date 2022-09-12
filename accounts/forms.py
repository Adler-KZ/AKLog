from django import forms
from django.contrib.auth import get_user_model

from allauth.account.forms import (
    SignupForm as AllauthSignupForm,
    LoginForm as AllauthLoginForm,
    ResetPasswordForm as AllauthResetPasswordForm,
    ResetPasswordKeyForm as AllauthResetPasswordKeyForm,
    ChangePasswordForm as AllauthChangePasswordForm,
    SetPasswordForm as AllauthSetPasswordForm,

)


class SignupForm(AllauthSignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def save(self, request):
        user = super().save(request)
        return user


class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def login(self, *args, **kwargs):
        return super(LoginForm, self).login(*args, **kwargs)


class SetPasswordForm(AllauthSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def save(self):
        super(SetPasswordForm, self).save()


class PasswordResetForm(AllauthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})

    def save(self, request):
        email_address = super(PasswordResetForm, self).save(request)
        return email_address


class ResetPasswordKeyForm(AllauthResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def save(self):
        email_address = super(ResetPasswordKeyForm, self).save()
        return email_address


class ChangePasswordForm(AllauthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def save(self):
        email_address = super(ChangePasswordForm, self).save()
        return email_address


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'bio', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not self.instance.is_superuser:
            self.fields['email'].disabled = True
