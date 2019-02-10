from django.urls import path
from .views.info import AccountView, InfoView, Login

urlpatterns = [
    # Info
    path('/me', AccountView.as_view(method=['GET'], STATUS=True)),
    path('/status', AccountView.as_view(method=['POST'], STATUS=True)),
    path('/register', AccountView.as_view(method=['POST'])),
    path('/<str:aid>', AccountView.as_view(method=['GET', 'PUT'])),
    path('/root/<str:aid>', InfoView.as_view(method=['GET'])),
    # 开发登陆接口
    path('/register/this/is/association/jiekou/useing/to/kaifa', Login.as_view(method=['POST'])),
]

