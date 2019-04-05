from .views import *

from django.urls import path, include



curriculum_urlpatterns = [
    path('', CurriculumInfo.as_view(method=['GET', 'PUT'])),
    path('/reset', CurriculumInfo.as_view(method=['GET'], RESET=True)),
    path('/manage', CurriculumView.as_view(method=['GET', 'POST'], SUMMARY=True)),
    path('/info', CurriculumView.as_view(method=['GET'])),
]

urlpatterns = [
    # 课表
    path('/curriculums', include(curriculum_urlpatterns))
]