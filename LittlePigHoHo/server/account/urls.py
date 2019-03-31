from django.urls import path
from .views import *

urlpatterns = [
    # Info
    path('/me', AccountView.as_view(method=['GET'], STATUS=True)),
    path('/status', AccountView.as_view(method=['POST'], STATUS=True)),
    path('/register', AccountView.as_view(method=['POST'])),
    path('/<int:aid>', AccountView.as_view(method=['GET', 'PUT'])),
    path('/root/<int:aid>', InfoView.as_view(method=['GET'])),
    path('/list', InfoView.as_view(method=['GET'], LIST=True)),
    path('/_mget', InfoView.as_view(method=['POST'])),
    # 开发登陆接口
    path('/register/this/is/jiekou/useing/to/kaifa', Login.as_view(method=['POST'])),
]

