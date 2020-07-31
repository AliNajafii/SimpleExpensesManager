from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('accounts',views.AccountViewSet,basename='account-info')
router.register('tags',views.TagInfoViewSet,basename='tag-info')

urlpatterns = []
urlpatterns += router.urls
