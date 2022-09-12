from django.urls import path
from allauth.account import views
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from .views import profile_view, subscription_view

urlpatterns = [
    # Allauth urls
    path('email/', RedirectView.as_view(url='/')),
    path('password/change/', views.PasswordChangeView.as_view(success_url=reverse_lazy('blogs:list')),
         name='account_change_password'),
    path('password/set/', views.PasswordSetView.as_view(success_url=reverse_lazy('blogs:list')),
         name='account_set_password'),

    # Local urls
    path('profile/', profile_view, name='account_profile'),
    path('subscription/', subscription_view, name='account_subscription'),
]
