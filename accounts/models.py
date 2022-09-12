from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    class Meta:
        permissions = [
            ('can_see_vip', 'Can see vip blogs')
        ]

    email = models.EmailField(_("Email"))
    bio = models.TextField(_("Bio"), max_length=250, blank=True)
    subscription_date = models.DateField(default=timezone.now)

    @property
    def subscription_to(self):
        return self.subscription_date - timezone.localtime(timezone.now()).date()

    def is_special_user(self):
        perm = Permission.objects.get(codename='can_see_vip')
        if self.has_perm('blogs.publish_blog') or self.subscription_to > timezone.timedelta(days=0):
            self.user_permissions.add(perm)
        else:
            self.user_permissions.remove(perm)


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(_("Ip address"), unique=True)

    def __str__(self):
        return self.ip
