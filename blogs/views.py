from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import BadRequest, PermissionDenied
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic

from .models import Blog
from .forms import BlogForm
from categories.models import Category
from .mixins import BlogFormFieldsMixin, BlogIpMixin, CreateUpdateFormValidMixin


def blog_list_view(request, author_username=None, category_slug=None):
    # Variables
    query = request.GET.get('q', '')
    page = request.GET.get('page', '1')
    author_name = None
    category_obj = None

    # Queries
    if author_username:
        author = get_object_or_404(get_user_model(), username=author_username)
        blogs = author.blogs.published()
        author_name = author.get_full_name() if author.get_full_name() else author.username
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        blogs = category.blogs.published()
        category_obj = category
    else:
        blogs = Blog.objects.published()

    # Pagination
    paginator = Paginator(blogs.filter(title__icontains=query), 5)
    blogs = paginator.page(page)
    page_range = paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)

    # Context
    context = {
        'query': query,
        'blogs': blogs,
        'page_range': page_range,
        'author_name': author_name,
        'category_obj': category_obj,
    }
    return render(request, 'blogs/list.html', context=context)


class BlogDetailView(UserPassesTestMixin, BlogIpMixin, generic.DetailView):
    def test_func(self):
        blog = self.get_object()
        user = self.request.user
        return blog.status == 'p' or blog.author == user or user.has_perm('blogs.publish_blog')

    model = Blog
    context_object_name = 'blog'
    template_name = 'blogs/detail.html'


class BlogCreateView(PermissionRequiredMixin, CreateUpdateFormValidMixin, BlogFormFieldsMixin, generic.CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/create.html'
    permission_required = 'blogs.add_blog'


class BlogUpdateView(UserPassesTestMixin, CreateUpdateFormValidMixin, PermissionRequiredMixin, BlogFormFieldsMixin,
                     generic.UpdateView):
    def test_func(self):
        blog = self.get_object()
        user = self.request.user
        return blog.author == user and blog.status == 'd' or user.is_superuser

    model = Blog
    form_class = BlogForm
    template_name = 'blogs/create.html'
    permission_required = 'blogs.change_blog'


class BlogDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Blog
    permission_required = "blogs.delete_blog"
    success_url = reverse_lazy('blogs:list')
    template_name = 'blogs/delete.html'


class BlogAuthorProfileView(PermissionRequiredMixin, generic.ListView):
    model = Blog
    paginate_by = 10
    context_object_name = 'blogs'
    template_name = 'blogs/author_blogs.html'
    permission_required = 'blogs.add_blog'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)


class BlogReviewView(PermissionRequiredMixin, generic.ListView):
    model = Blog
    paginate_by = 10
    context_object_name = 'blogs'
    template_name = 'blogs/review.html'
    permission_required = 'blogs.publish_blog'

    def get_queryset(self):
        return Blog.objects.filter(status='r')

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=request.POST.get('blog_id'))
        if blog.status == 'r':
            if '1' in request.POST:
                blog.status = 'p'
            elif '0' in request.POST:
                blog.status = 'd'
            else:
                raise BadRequest('Bad request')
            blog.save()
            return redirect('blogs:review')
        raise PermissionDenied()
