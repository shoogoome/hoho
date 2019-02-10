from django.urls import path
from .views.department import DepartmentInfo
from .views.info import AssociationInfoView, AssociationVerification
from .views.attendance import AttendanceView, AttendanceSign, AttendanceManage

urlpatterns = [
    path('', AssociationInfoView.as_view(method=['POST'])),
    path('/list', AssociationInfoView.as_view(method=['GET'])),
    path('/<str:aid>', AssociationInfoView.as_view(method=['PUT', 'DELETE', 'GET'])),
    path('/<str:aid>/recode', AssociationVerification.as_view(method=['GET'])),
    path('/<str:aid>/apply', AssociationVerification.as_view(method=['GET'], APPLY=True)),
    path('/<str:aid>/verification', AssociationVerification.as_view(method=['PUT'])),
    # Attendance
    path('/<str:aid>/attendance', AttendanceView.as_view(method=['GET'])),
    path('/<str:aid>/attendance/create', AttendanceView.as_view(method=['POST'])),
    # Department
    path('/<str:aid>/department', DepartmentInfo.as_view(method=['POST'])),
    path('/<str:aid>/department/<str:did>', DepartmentInfo.as_view(method=['GET', 'PUT', 'DELETE'])),
    # Sign
    path('/<str:aid>/attendance/<str:vid>', AttendanceSign.as_view(method=['GET', 'POST'])),
    path('/<str:aid>/attendance/<str:vid>/leave', AttendanceManage.as_view(method=['GET'])),
    path('/<str:aid>/attendance/<str:vid>/manage', AttendanceManage.as_view(method=['POST'])),
]