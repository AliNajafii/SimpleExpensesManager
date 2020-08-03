"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework_jwt import views
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('athentication.urls')),
    path('',include('athentication.user_urls')),
    path('analytics/',include('analytics.urls')),
    path('account/',include('account.urls') ),
    path('search/', search_views.SearchAPIView.as_view(),name='search' ),


]
