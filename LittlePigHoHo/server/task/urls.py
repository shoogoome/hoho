from .views import *

from django.urls import path


urlpatterns = [
    # Task
    path('', TaskInfo.as_view(method=['POST'])),
    path('/<int:tid>', TaskInfo.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', TaskView.as_view(method=['GET'])),
    path('/_mget', TaskView.as_view(method=['POST'])),
    # Report
    path('/<int:tid>/report', TaskReportView.as_view(method=['GET', 'POST', 'PUT', 'DELETE']))
]