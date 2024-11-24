"""
ASGI config for ass4 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.consumers import AudioProgressConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ass4.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/audio_progress/<int:upload_id>/', AudioProgressConsumer.as_asgi()),
        ])
    ),
})
