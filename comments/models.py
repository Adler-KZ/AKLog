from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class CommentManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class Comment(models.Model):
    SCORE_CHOICES = (
        (1, _("Very bad")),
        (2, _("Bad")),
        (3, _("Normal")),
        (4, _("Good")),
        (5, _("Very good")),
    )
    text = models.TextField(_('Text'))
    name = models.CharField(_('Full name'), max_length=50)
    email = models.EmailField(_("Email"))
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE, related_name='comments', verbose_name=_('Blog'))
    is_active = models.BooleanField(_("Is active"), default=True)
    score = models.IntegerField(_("Score"), default=3, choices=SCORE_CHOICES,
                                validators=[MaxValueValidator(5), MinValueValidator(1)])
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commented by {self.name} on {self.blog}'

    class Meta:
        ordering = ['-datetime_created']

    objects = CommentManager()
