from channels.routing import ProtocolTypeRouter, URLRouter
#from django.conf.urls import url
from django.urls import re_path
#from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from Students_Management.consumers import StudentRegPortal_Consumer
from Attendance_Management.consumers import AttPortal_Consumer

application = ProtocolTypeRouter({
    #Empty 
    #"http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
                URLRouter(
                [
                    re_path(r"^student-fprint-socket-portal", StudentRegPortal_Consumer.as_asgi()),
                    re_path(r"^student-attendance-socket-portal", AttPortal_Consumer.as_asgi()),
                    #url(r"^user-notifications-portal/(?P<deviceNo>)", User_Dev_Portal.as_asgi()),
                    #url(r"^user-notifications-portal/(?P<deviceNo>)", User_Dev_Portal.as_asgi()),
                ]
            )
        )
    )
})