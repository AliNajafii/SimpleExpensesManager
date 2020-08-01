from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from account import models as account_models
from django.core import exceptions as django_exceptions
from . import serializer
from rest_framework.response import Response
from rest_framework import status
from account.account_views import URLQueryParamsMixin


class AccountViewSet(viewsets.ViewSet,URLQueryParamsMixin):
    lookup_field = 'name'
    authentication_classes = (BasicAuthentication,)
    serializer_class = serializer.AccountInfoSerializer

    def get_queryset(self):
        user = self.request.user
        return user.account_set.all()

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name = self.kwargs.get('name'))
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass
    def get_serializer(self,*args,**kwargs):
        if self.serializer_class:
            return self.serializer_class(
                context={'request':self.request},
                *args,
                **kwargs
                )
        return serializer.AccountInfoSerializer(
             context={'request':self.request},
                *args,
                **kwargs
        )

    @action(['GET'],detail=True,url_path='info')
    def info(self,request,pk=None,**kwargs):
        account = self.get_object()
        time = self.get_time_from_query(request)
        if account:
            seri = self.get_serializer(account)
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class TagInfoViewSet(viewsets.ViewSet):
    lookup_field = 'name'
    serializer_class = serializer.TagInfoSerializer
    authentication_classes = [BasicAuthentication,]

    def get_queryset(self):
        return self.request.user.tag_set.all()

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name= self.kwargs.get('name'))
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass

        except django_exceptions.MultipleObjectsReturned:
            pass
    
    def get_serializer(self,*args,**kwargs):
        if self.serializer_class:
            return self.serializer_class(
                context={'request':self.request},
                *args,
                **kwargs
                )
        return serializer.TagInfoSerializer(
            context={'request':self.request},
                *args,
                **kwargs
        )

    @action(['GET'],detail=True,url_path='info')
    def info(self,request,pk=None,**kwargs):
        obj = self.get_object()
        # time = self.get_time_from_query(request)
        if obj:
            seri = self.get_serializer(obj)
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryInfoViewSet(viewsets.ViewSet):
    lookup_field = 'name'
    serializer_class = serializer.CategroryInfoSerializer
    authentication_classes = [BasicAuthentication,]

    def get_queryset(self):
        return self.request.user.category_set.all()

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name= self.kwargs.get('name'))
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass

        except django_exceptions.MultipleObjectsReturned:
            pass

    def get_serializer(self,*args,**kwargs):
        if self.serializer_class:
            return self.serializer_class(
                context={'request':self.request},
                *args,
                **kwargs
                )


    @action(['GET'],detail=True,url_path='info')
    def info(self,request,pk=None,**kwargs):
        obj = self.get_object()
        # time = self.get_time_from_query(request)
        if obj:
            seri = self.get_serializer(obj)
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
