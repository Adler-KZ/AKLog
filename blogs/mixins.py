from django.shortcuts import redirect
from django.urls import reverse_lazy


class BlogFormFieldsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BlogIpMixin:
    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.hits.add(request.user.ip_address)
        # BlogIp.objects.get_or_create(blog=blog, ip=request.user.ip_address)
        return super().get(request, *args, **kwargs)


class CreateUpdateFormValidMixin:
    # <- Way 1 -->
    def form_valid(self, form):
        blog = form.save(commit=False)

        if not self.request.user.is_superuser:
            blog.author = self.request.user

        form.save()

        # add and save all categories parent
        categories = form.cleaned_data['categories']
        for category in categories:
            while category.parent:
                category = category.parent
                blog.categories.add(category)

        return redirect(reverse_lazy('blogs:author'))

    # <- Way 2 -->
    # def form_valid(self, form):
    #     blog = form.save(commit=False)
    #
    #     # add and save all categories parent
    #     form.save_m2m()
    #     categories = form.cleaned_data['categories']
    #     for category in categories:
    #         while category.parent:
    #             category = category.parent
    #             blog.categories.add(category)
    #
    #     if not self.request.user.is_superuser:
    #         blog.author = self.request.user
    #
    #     blog.save()
    #     return redirect('blogs:author')
