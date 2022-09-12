from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['name', 'email', 'text', 'score']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Full name'), 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': _('Your email'), 'class': 'form-control'}),
            'score': forms.Select(attrs={'class': 'form-group nice-select'}),
            'text': forms.Textarea(attrs={'placeholder': _('Write your message'), 'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields.pop('name')
            self.fields.pop('email')
