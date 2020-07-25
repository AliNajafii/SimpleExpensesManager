from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics
from django.core import exceptions as django_exceptions
from . import serialization
from .account_views import URLQueryParamsMixin
from rest_framework.response import Response
from rest_framework import status

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.CategorySerializer
    http_method_names = ['get','put','delete',]

    def get_queryset(self,*args,**kwargs):
        return self.request.user.category_set.all()

    def get_object(self):
        cat_name = self.kwargs.get('cat_name')
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name= cat_name)
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass


class CategoryListView(generics.ListAPIView,URLQueryParamsMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.CategorySerializer
    order_by = '-date'

    def get_queryset(self):
        return self.request.user.category_set.all().order_by(self.order_by)

    def get_serializer(self,*args,**kwargs):
        fields = self.get_fields_from_query(self.request)
        query = self.get_queryset()
        return self.serializer_class(query,fields=fields,context={'request':self.request},many=True)


class CategoryCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.CategorySerializer
    http_method_names = ['post']

    def get_queryset(self):
        return self.request.user.category_set.all()
