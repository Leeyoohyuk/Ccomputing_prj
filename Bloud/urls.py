"""Bloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from web.views import oAuth_signup

SOCIAL_AUTH_URL_NAMESPACE = 'social'
LOGIN_REDIRECT_URL='/list/' # JYW redirect path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('web.urls'), name='home'),
    url(r'^login_check/', oAuth_signup, name='check'),
#    url(r'^accounts/logout/$', views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/home/'}),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]
