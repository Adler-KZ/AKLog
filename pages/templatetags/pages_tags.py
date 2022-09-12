from django import template
from django.contrib.auth import get_user_model

from categories.models import Category

register = template.Library()


@register.inclusion_tag('partial/pages/navbar.html', takes_context=True)
def navbar(context):
    authors = get_user_model().objects.filter(groups__name__in=['author'])
    categories = Category.objects.parents()
    return {
        'user': context['user'],
        'categories': categories,
        'authors': authors
    }
