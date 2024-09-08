from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.getData),
    path('add-item/', views.addItem)
]