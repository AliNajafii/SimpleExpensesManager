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

    @action(['GET'],detail=True,url_path='transaction-num')
    def get_transactions_num(self,request,pk=None,**kwargs):
        account = self.get_object()
        if account:
            seri = self.serializer_class(account,fields=('transaction_number',))
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['GET'],detail=True,url_path='expenses')
    def get_expense_transactions(self,request,pk=None,**kwargs):
        account = self.get_object()
        if account:
            seri = self.serializer_class(account,fields=('expense',))
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['GET'],detail=True,url_path='incomes')
    def get_income_transactions(self,request,pk=None,**kwargs):
        account = self.get_object()
        if account:
            seri = self.serializer_class(account,fields=('income',))
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['GET'],detail=True,url_path='last-month-income-avg')
    def last_month_income_avg(self,request,pk=None,**kwargs):
        account = self.get_object()
        if account:
            seri = self.serializer_class(account,fields=(self.action,))
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['GET'],detail=True,url_path='last-time-income-avg')
    def last_time_income_avg(self,request,pk=None,**kwargs):
        account = self.get_object()
        time = self.get_time_from_query(request)
        if account:
            seri = self.serializer_class(account,fields=(self.action,),context={'time':time})
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['GET'],detail=True,url_path='last-time-expense-avg')
    def last_time_expense_avg(self,request,pk=None,**kwargs):
        account = self.get_object()
        time = self.get_time_from_query(request)
        if account:
            seri = self.serializer_class(account,fields=(self.action,),context={'time':time})
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['GET'],detail=True,url_path='info')
    def info(self,request,pk=None,**kwargs):
        account = self.get_object()
        time = self.get_time_from_query(request)
        if account:
            seri = self.serializer_class(account,context={'time':time})
            return Response(seri.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
        
