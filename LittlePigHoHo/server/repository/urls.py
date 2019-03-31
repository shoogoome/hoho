from django.urls import path
from server.repository.views.resources.youku import Resources


urlpatterns = [
    # Photo
    path('/balabalamiaomiaomiao', Resources.as_view(method=['GET'])),
]
