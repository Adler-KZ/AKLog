from django import template
from django.db.models import Avg, Count, Q
from datetime import timedelta, datetime

from blogs.models import Blog

register = template.Library()


@register.inclusion_tag('partial/blogs/top_month.html')
def top_month_blogs():
    last_month = datetime.now() - timedelta(days=30)
    blogs = Blog.objects.published().annotate(
        count=Count('hits', filter=Q(blogip__datetime_created__gt=last_month))) \
                .order_by('-count', '-datetime_modified')[:5]
    return {
        'blogs': blogs,
    }


@register.inclusion_tag('partial/blogs/best.html')
def best_blogs():
    blogs = Blog.objects.published().filter(comments__isnull=False).annotate(
        score=Avg('comments__score', filter=Q(comments__is_active=True))).order_by(
        '-score')[:5]
    return {
        'blogs': blogs,
    }
