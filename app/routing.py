from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path
import app.picture.consumers as apc
import app.audio.consumers as aac
import app.draw.consumers as adc

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
	URLRouter([
	    re_path(r'^ws/audio/$', aac.AudioConsumer),
            re_path(r'^ws/draw/$', adc.DrawConsumer),
	    re_path(r'^ws/picture/$', apc.PictureConsumer),
	])
        )
    )
})
