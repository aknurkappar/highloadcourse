from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello),
    path("posts/", views.get_posts),
    path("posts/<int:id>/", views.get_post_by_id),
]