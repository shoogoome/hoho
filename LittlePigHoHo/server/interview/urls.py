from django.urls import path, include
from .views import *


registration_urlpatterns = [
    path('', RegistrationInfo.as_view(method=['POST'])),
    path('/<int:rid>', RegistrationInfo.as_view(method=['GET', 'DELETE'])),
    path('/list', RegistrationView.as_view(method=['GET'])),
    path('/_mget', RegistrationView.as_view(method=['POST'])),
]


urlpatterns = [
    # 模板
    path('', RegistrationTemplateInfo.as_view(method=['POST'])),
    path('/<int:rtid>', RegistrationTemplateInfo.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', RegistrationTemplateView.as_view(method=['GET'])),
    path('/_mget', RegistrationTemplateView.as_view(method=['POST'])),
    # 报名
    path('/registrations', include(registration_urlpatterns)),
    # 管理
    path('/manage', InterviewManage.as_view(method=['GET', 'POST'], FILTER=False)),
    path('/filter', InterviewManage.as_view(method=['POST'])),
]