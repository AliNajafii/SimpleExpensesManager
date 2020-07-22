from rest_framework_jwt import views
from django.urls import include,path

urlpatterns = [

    path('login',views.obtain_jwt_token),
    path('refresh-token',views.refresh_jwt_token),

]
