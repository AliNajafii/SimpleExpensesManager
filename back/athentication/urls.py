from rest_framework_jwt import views
from django.urls import include,path
from . import views as auth_view
from djoser.views import TokenCreateView,TokenDestroyView
from .views import TokenLogout
urlpatterns = [
    path('token/login/',TokenCreateView.as_view()),
    path('token/logout/',TokenLogout.as_view())

]
