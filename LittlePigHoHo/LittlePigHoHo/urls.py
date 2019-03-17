"""LittlePigHoHo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from server.repository.urls import urlpatterns as repository_urlpatterns
from server.account.urls import urlpatterns as account_urlpatterns
from server.school.urls import urlpatterns as school_urlpatterns
from server.association.urls import urlpatterns as association_urlpatterns
from server.homepage.views import home

urlpatterns = [
    path('', home),
    path('server_admin/', admin.site.urls),
    # path('repository', include(repository_urlpatterns)),
    path('account', include(account_urlpatterns)),
    path('school', include(school_urlpatterns)),
    # path('association', include(association_urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
