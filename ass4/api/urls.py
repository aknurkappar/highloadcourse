from django.urls import path
from . import views
from .views import EmailViewSet, TwoFactorAuthViewSet,TestViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'email', EmailViewSet, basename='email')
router.register('auth', TwoFactorAuthViewSet, basename='auth')
router.register('', TestViewSet, basename='test')

urlpatterns = [
    *router.urls,
    path('upload-audio/', views.upload_audio, name='upload_audio'),
    path('progress/<int:upload_id>/', views.audio_progress, name='audio_progress')
]
