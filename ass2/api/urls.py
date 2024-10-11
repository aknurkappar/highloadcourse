# urls.py
from django.urls import path
from .views import (
    posts,
    add_user,
    add_tag,
    add_comment,
    comments_by_post,
    posts_view_level_cache,
    post_by_id_low_level,
    PostListView,
    PostDetailView,
)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('users/', add_user, name='add-user'),
    path('tags/', add_tag, name='add-tag'),
    path('posts/', posts, name='add-post'),
    path('posts/view-level-caching', cache_page(60)(posts_view_level_cache), name='posts-view-level-caching'),
    path('posts/template', PostListView.as_view(), name='posts-template'),
    path('posts/template/<int:pk>', PostDetailView.as_view(), name='post-details-template'),
    path('posts/low-level/<int:pk>', post_by_id_low_level, name='post-by-id-low-level'),
    path('posts/<int:post_id>/comments', comments_by_post, name='comments-by-post'),
    path('comments/', add_comment, name='add-comment'),
]
