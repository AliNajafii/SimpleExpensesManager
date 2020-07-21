from django.urls import path,include
from . import cat_views

urlpatterns = [

    path('<str:cat_name>',cat_views.CategoryDetailView.as_view(),name='cat-detail'),
    path('lists',cat_views.CategoryListView.as_view()),
    path('create',cat_views.CategoryCreateView.as_view()),
    path('delete',cat_views.CategoryDeleteView.as_view()),


]
