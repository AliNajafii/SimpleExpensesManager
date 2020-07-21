from django.urls import path,include
from . import tag_views

urlpatterns = [

    path('<str:tag_name>',tag_views.TagDetailView.as_view(),name='tag-detail'),
    path('lists',tag_views.TagListView.as_view()),
    path('create',tag_views.TagCreateView.as_view()),
    path('delete',tag_views.TagDeleteView.as_view()),


]
