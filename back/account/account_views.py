from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework import exceptions as rest_exceptions
from django.contrib.auth import get_user_model
from django.core import exceptions as django_exceptions
from rest_framework.response import Response
from rest_framework import status
from . import serialization
from rest_framework.renderers import JSONRenderer
from . import serialization
from . import models

class URLQueryParamsMixin(object):
    """
    this class is for customizing serializer
    by clients within query param
    """
    fields_query_kwarg = 'fields'
    time_fileds = ['years','months','weeks','days']

    def get_fields_from_query(self,request):
        fields = request.query_params.get(self.fields_query_kwarg)
        if fields:
            fields = f',{fields}'.split(',') # for avoiding none functionality
            return tuple(fields)

    def get_time_from_query(self,request):
        qp = request.query_params
        time_params = {}
        for time in self.time_fileds:
            if qp.get(time):
                number = int(qp.get(time))
                time_params.update({time:number})

        return time_params



class AccountCreateView(generics.CreateAPIView):
    serializer_class = serialization.AccountSerializer
    model = models.Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return self.request.user.account_set.all()
    
    def get_serializer(self,*args,**kwargs):
        context = {
            'request': self.request
        }
        if self.serializer_class:
            return serializer_class(
                context=context,
                *args,
                **kwargs
                )
        return serialization.AccountSerializer(
            context=context,
            *args,
            **kwargs
        )
            

class AccountProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    USER = get_user_model()

    
    def get_serializer(self,*args,**kwargs):
        context = {
            'request':self.request,
            }
        if self.serializer_class:
            return self.serializer_class(
                context=context
                *args,
                **kwargs
                )
        return serialization.AccountSerializer(
            context=context,
            *args,
            **kwargs
            )
    
    def get_queryset(self):
        return self.request.user.account_set.all()
    
    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name=self.kwargs.get('account_name'))
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass
    
    def retrieve(self,request,*args,**kwargs):
        obj = self.get_object()
        if obj:
            seri = self.get_serializer(obj)
            return Response(seri.data)
        
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    def update(self,request,*args,**kwargs):
        obj = self.get_object()
        if obj :
            seri = self.get_serializer(obj,data=request.data)
            if seri.is_valid():
                seri.save()
                return Response(seri.data)
            return Response(seri.errors)
        return Response(status= status.HTTP_404_NOT_FOUND)

    

    

class UserAccountListView(generics.ListAPIView):
    serializer_class = serialization.AccountSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args,**kwargs):
        return self.request.user.account_set.all()

    def get_serializer(self,*args,**kwargs):
        # client can choose the field for json representation
        seri = None
        query = self.get_queryset()
        seri = serialization.AccountSerializer(
                query,
                many=True,
                context = {'request':self.request}
            )

        return seri





# --------------------Transactions-------------------------



class TransactionCreateView(generics.CreateAPIView):
    serializer_class = serialization.TransactionSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = models.Transaction

    def get_serializer(self,*args,**kwargs):
        name = self.kwargs.get('account_name')
        account =  self.request.user.account_set.get(name=name)
        if self.serializer_class:
            return self.serializer_class(
                context={
                    'account':account,
                    'request':self.request,
                    'is_making_transaction':True
                    },
                *args,
                **kwargs)
        return serialization.TransactionSerializer(*args,**kwargs)


    def get_queryset(self):
        name = self.kwargs.get('account_name')
        try:
            account =  self.request.user.account_set.get(name=name)
            return account.transaction_set.all()
        except django_exceptions.ObjectDoesNotExist:
            pass

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(name=self.kwargs.get('name'))
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serialization.TransactionSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_serializer(self,*args,**kwargs):
        if self.serializer_class:
            return self.serializer_class(context={'request':self.request},*args,**kwargs)
        return serialization.TransactionSerializer(fields=fileds,*args,**kwargs)


    def get_queryset(self):
        name = self.kwargs.get('account_name')
        try:
            account =  self.request.user.account_set.get(name=name)
            return account.transaction_set.all()
        except django_exceptions.ObjectDoesNotExist:
            pass

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(id= self.kwargs.get('trans_id'))
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass


class TransactionListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.TransactionSerializer
    pagination_class = LimitOffsetPagination
    order_by = '-date'

    def get_queryset(self,*args,**kwargs):
        acc_name = kwargs.get('account_name')
        try:
            account = self.request.user.account_set.get(name= acc_name)
            return account.transaction_set.all().order_by(self.order_by)
        except django_exceptions.ObjectDoesNotExist :
            pass
    def get_serializer(self,*args,**kwargs):
        cls = self.serializer_class
        query = self.get_queryset(*args,**kwargs)
        return cls(query,many=True)

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        if queryset :

            serializer = self.get_serializer(queryset,many=True)
            return Response(serializer.data)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
