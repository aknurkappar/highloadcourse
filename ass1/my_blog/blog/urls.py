from django.urls import path
from .views import HelloView, PostListView, PostDetailView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
]