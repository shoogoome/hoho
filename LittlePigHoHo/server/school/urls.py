from django.urls import path, include
from .views.info import SchoolView, SchoolList
from server.association.urls import urlpatterns as association_urlpatterns


urlpatterns = [
    path('', SchoolView.as_view(method=['POST'])),
    path('/list', SchoolList.as_view(method=['GET'])),
    path('/_mget', SchoolList.as_view(method=['POST'])),
    path('/<int:sid>', SchoolView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:sid>/associations', include(association_urlpatterns)),
]