from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .forms import SignupForm, ProfileForm


def signup_view(request):
    form = SignupForm()
    context = {'form': form, }
    return render(request, 'account/signup.html', context)


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()

    return render(request, 'account/profile.html', {'form': form})


@login_required()
def subscription_view(request):
    if request.method == 'POST':
        plan = request.POST.get('p')
        if plan.isnumeric():
            user = request.user
            user.subscription_date += timezone.timedelta(days=int(plan))
            user.save()

    return render(request, 'account/subscription.html', )
