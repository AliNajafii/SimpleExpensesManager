from django.urls import path
from . import views as auth_view
urlpatterns = [

    # path('login',auth_view.JWTLoginView.as_view()),
    # path('refresh-token',views.refresh_jwt_token),
    # path('logout',auth_view.JWTLogoutView.as_view()),
    path('user-crud/<str:username>',auth_view.UserDetailView.as_view())


]
