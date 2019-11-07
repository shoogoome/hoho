from django.urls import path, include
from server.notice.urls import urlpatterns as notice_urlpatterns
from server.task.urls import urlpatterns as task_urlpatterns
from server.appraising.urls import urlpatterns as appraising_urlpatterns
from server.interview.urls import urlpatterns as interview_urlpatterns
from server.scheduling.urls import urlpatterns as scheduling_urlpatterns

from .views import *


# 协会用户路由
account_urlpatterns = [
    path('', AssociationAccountInfo.as_view(method=['POST', 'PUT', 'DELETE'])),
    path('/me', AssociationAccountInfo.as_view(method=['GET'], ME=True)),
    path('/<int:acid>', AssociationAccountInfo.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', AssociationAccountView.as_view(method=['GET'])),
    path('/_mget', AssociationAccountView.as_view(method=['POST'])),
]

# 协会部门路由
department_urlpatterns = [
    path('', DepartmentInfo.as_view(method=['POST'])),
    path('/list', DepartmentView.as_view(method=['GET'])),
    path('/_mget', DepartmentView.as_view(method=['POST'])),
    path('/<int:did>', DepartmentInfo.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:did>/add', DepartmentMatters.as_view(method=['POST'])),
]

# 考勤路由
attendance_urlpatterns = [
    # 考勤表信息
    path('', AttendanceView.as_view(method=['POST'])),
    path('/<int:vid>', AttendanceView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', AttendanceInfo.as_view(method=['GET'])),
    path('/_mget', AttendanceInfo.as_view(method=['POST'])),
    # 签到
    path('/<int:vid>/sign', AttendanceSign.as_view(method=['GET', 'POST'])),
    # 管理
    path('/<int:vid>/leave', AttendanceManage.as_view(method=['POST'])),
    path('/<int:vid>/manage', AttendanceManager.as_view(method=['POST'])),
]

# 主路由
urlpatterns = [
    # 协会
    path('', AssociationInfoView.as_view(method=['POST'])),
    path('/list', AssociationVerification.as_view(method=['GET'], LIST=True)),
    path('/_mget', AssociationVerification.as_view(method=['POST'])),
    path('/<int:aid>', AssociationInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:aid>/recode', AssociationVerification.as_view(method=['GET'])),
    # 协会用户
    path('/<int:aid>/accounts', include(account_urlpatterns)),
    # 部门
    path('/<int:aid>/departments', include(department_urlpatterns)),
    # 考勤
    path('/<int:aid>/attendances', include(attendance_urlpatterns)),
    # 通知
    path('/<int:aid>/notices', include(notice_urlpatterns)),
    # 任务
    path('/<int:aid>/tasks', include(task_urlpatterns)),
    # 绩效考核
    path('/<int:aid>/appraisings', include(appraising_urlpatterns)),
    # 招新模块
    path('/<int:aid>/interviews', include(interview_urlpatterns)),
    path('/<int:aid>/schedulings', include(scheduling_urlpatterns)),
]
