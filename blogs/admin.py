from django.contrib import admin

from .models import Blog, BlogIp
from comments.models import Comment


class BlogIpInline(admin.TabularInline):
    model = BlogIp
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['name', 'text', 'score', 'is_active','parent']
    extra = 1


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'is_vip', 'cover_tag']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']

    inlines = [
        BlogIpInline,
        CommentInline,
    ]


# admin.site.register(BlogIp)
