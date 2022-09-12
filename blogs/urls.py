from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    # List of blogs urls
    path('', views.blog_list_view, name='list'),
    path('author/<slug:author_username>/', views.blog_list_view, name='author_list'),
    path('category/<slug:category_slug>/', views.blog_list_view, name='category'),

    # CRUD urls
    path('create/', views.BlogCreateView.as_view(), name='create'),
    path('detail/<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('update/<slug:slug>/', views.BlogUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='delete'),

    # Author & Admin urls
    path('my-blogs/', views.BlogAuthorProfileView.as_view(), name='author'),
    path('review/', views.BlogReviewView.as_view(), name='review'),
]
