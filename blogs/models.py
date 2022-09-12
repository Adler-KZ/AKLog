from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.html import format_html


class BlogManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Blog(models.Model):
    STATUS_CHOICES = (
        ('d', _("Draft")),
        ('p', _("Public")),
        ('r', _("Review")),
    )

    class Meta:
        ordering = ['-datetime_modified']
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        permissions = [
            ('publish_blog', 'Can publish blog'),
        ]

    title = models.CharField(_('Title'), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    content = models.TextField(_('Content'), )
    categories = models.ManyToManyField('categories.Category', related_name='blogs', verbose_name=_("Categories"))
    cover = models.ImageField(_('Cover'), upload_to='covers/')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blogs',
                               verbose_name=_("Author"))
    status = models.CharField(_("Status"), max_length=1, choices=STATUS_CHOICES)
    is_vip = models.BooleanField(_("Vip blog"), default=False)
    hits = models.ManyToManyField('accounts.IpAddress', related_name='blogs', through='BlogIp', verbose_name=_("Hits"))
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'slug': self.slug})

    def cover_tag(self):
        return format_html(
            f"<img width=65 height=65 style='object-fit: contain; border-radius:3px' src='{self.cover.url}'>")

    cover_tag.short_description = _('Cover')

    @property
    def avg_score(self):
        scores = self.comments.filter(is_active=True).aggregate(Avg('score'))
        if not scores['score__avg']:
            return 0
        return scores['score__avg']

    @property
    def total_hits(self):
        return self.hits.all().count()

    objects = BlogManager()


class BlogIp(models.Model):
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)
    ip = models.ForeignKey('accounts.IpAddress', on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
