from .views import *

from django.urls import path


urlpatterns = [
    path('', NoticeInfo.as_view(method=['POST'])),
    path('/<int:nid>', NoticeInfo.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', NoticeView.as_view(method=['GET'])),
    path('/_mget', NoticeView.as_view(method=['POST'])),
]