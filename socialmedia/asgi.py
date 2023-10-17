import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
django.setup()

from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from .channelsmiddleware import JwtAuthMiddleware
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat import routing



from posts import routing as postrouting

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': JwtAuthMiddleware(URLRouter(routing.websocket_urlpatterns + postrouting.websocket_urlpatterns)
        )
    }
)
