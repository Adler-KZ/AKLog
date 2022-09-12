from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'categories', 'cover', 'is_vip', 'status', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Title'), 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'placeholder': _('Slug'), 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': _('content'), 'rows': 5, 'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'style': 'height:150px;'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = get_user_model().objects.filter(groups__name__in=['author'])
        if not user.is_superuser:
            self.fields.pop('author')
            self.fields['status'].choices = [
                ('d', _("Draft")),
                ('r', _("Review")),
            ]
