from django import template

from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('partial/comments/comments.html', takes_context=True)
def blog_comments(context):
    user = context['user']
    slug = context['blog'].slug
    comments = Comment.objects.active().filter(blog__slug=slug, parent__isnull=True)
    comment_form = CommentForm(user=user)
    return {
        'user': user,
        'comments': comments,
        'form': comment_form,
        'slug': slug,
        'messages': context['messages'],
    }
