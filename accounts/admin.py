from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, IpAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser']
    filter_horizontal = ['groups', 'user_permissions']

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'bio')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("subscription_date", "last_login", "date_joined")}),
    )


admin.site.register(IpAddress)
