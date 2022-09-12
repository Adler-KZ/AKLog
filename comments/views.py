from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from .models import Comment
from .forms import CommentForm
from blogs.models import Blog


class CommentCreate(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def get_form_kwargs(self):
        kwargs = super(CommentCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        comment = form.save(commit=False)

        # parent comment
        parent_id = form.cleaned_data['parent']
        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)
            if not parent_comment.parent:
                comment.parent = parent_comment

        if self.request.user.is_authenticated:
            comment.name = self.request.user.username
            comment.email = self.request.user.email
        comment.blog = blog
        comment.save()

        return redirect('blogs:detail', self.kwargs['slug'])
