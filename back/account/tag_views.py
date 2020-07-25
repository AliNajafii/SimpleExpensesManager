from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .account_views import URLQueryParamsMixin
from . import serialization
from django.core import exceptions as django_exceptions
from . import models

class TagDetailView(generics.RetrieveUpdateDestroyAPIView,URLQueryParamsMixin):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.TagSerializer

    def get_object(self):
        tag_name = self.kwargs.get('tag_name')
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name = tag_name)
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass

    def get_queryset(self,*args,**kwargs):

        return self.request.user.tag_set.all().order_by('-date')

    def get_serializer(self,*args,**kwargs):
        seri = self.serializer_class
        fields = self.get_fields_from_query(self.request)
        return seri(fields=fields,*args,**kwargs)

    def retrieve(self,request,*args,**kwargs):

        obj = self.get_object()
        if obj :
            seri = self.get_serializer(obj)
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self,request,*args,**kwargs):
        obj = self.get_object()
        if obj:
            seri = self.get_serializer(obj,
            data=request.data,
            context={'request':request}
            )
            if seri.is_valid():
                seri.save()
                return Response(seri.data)
            return Response(seri.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request,*args,**kwargs):
        obj = self.get_object()
        if obj:
            obj.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class TagListView(generics.ListAPIView,URLQueryParamsMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.TagSerializer
    order_by = '-date'

    def get_queryset(self,*args,**kwargs):
        return models.Tag.objects.filter(user=self.request.user).order_by(self.order_by)


    def get_serializer(self,*args,**kwargs):
        fields = self.get_fields_from_query(self.request)
        return self.serializer_class(fields=fields,*args,**kwargs)

class TagCreateView(generics.CreateAPIView,URLQueryParamsMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.TagSerializer

    def get_serializer(self,*args,**kwargs):
        fields = self.get_fields_from_query(self.request)
        return self.serializer_class(fields=fields,context={'request':self.request},*args,**kwargs)
