from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CategoryManager(models.Manager):
    def parents(self):
        return self.filter(parent__isnull=True)

    def active(self):
        return self.filter(is_active=True)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', blank=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:category', args=(self.slug,))

    objects = CategoryManager()
