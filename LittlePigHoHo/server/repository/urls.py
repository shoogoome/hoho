from django.urls import path
from server.repository.views.photo.info import PhotoView, PhotoGet


urlpatterns = [
    # Photo
    path('/photo/<str:tid>', PhotoGet.as_view(method=['GET'])),
    path('/photo/upload/<str:tid>', PhotoView.as_view(method=['POST'])),
    path('/photo/list/<str:tid>', PhotoView.as_view(method=['GET'])),

]
