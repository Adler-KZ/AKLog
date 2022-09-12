from django.shortcuts import render, redirect

from .forms import ContactForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect('blogs:list')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', context={'form': form})


def home_view(request):
    return redirect('blogs:list')
