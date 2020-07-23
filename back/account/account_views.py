from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions as rest_exceptions
from django.contrib.auth import get_user_model
from django.core import exceptions as django_exceptions
from rest_framework.response import Response
from rest_framework import status
from . import serialization
from rest_framework.renderers import JSONRenderer
from . import serialization
from . import models


class AccountCreateView(generics.CreateAPIView):
    serializer_class = serialization.AccountSerializer
    model = models.Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)



    def post(self,request,*args,**kwargs):

        seri = serialization.AccountSerializer(data=request.data,
        context={'user':request.user,'request':request})
        if seri.is_valid():
            seri.save()
            account = seri.instance
            request.user.account_set.add(account)
            return Response(
            data=seri.data,
            status= status.HTTP_201_CREATED
            )
        return Response(
        data= seri.errors,
        status= status.HTTP_400_BAD_REQUEST
        )

class AccountProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    USER = get_user_model()
    renderer_classes = (JSONRenderer,)
    def get(self,request,*args,**kwargs):
        try :
            user = request.user
            account = user.account_set.get(name = kwargs.get('account_name'))
            seri = serialization.AccountSerializer(account,fields=('balance','transaction_set',),context={'transaction_fields':('amount',)})
            res = Response(data= seri.data,status=status.HTTP_200_OK)

            return res
        except django_exceptions.ObjectDoesNotExist :
            return Response(
            data={'error':'username or account  not found.'},
            status= status.HTTP_400_BAD_REQUEST
            )

    def http_method_not_allowed(self,request,*args,**kwargs):
        if not request.method == 'GET':
            raise MethodNotAllowed(method=request.method)

class UserAccountListView(generics.ListAPIView):

    authentication_classes = (BasicAuthentication,)

    def get_queryset(self,*args,**kwargs):
        return self.request.user.account_set.all()

    def get_serializer(self,*args,**kwargs):
        # client can choose the field for json representation
        query_fields = self.request.query_params.get('fields')

        seri = None
        query = self.get_queryset()
        context = {}

        if query_fields:
            query_fields = f',{query_fields}' # for avoiding none functionality
            context['fields'] = query_fields.split(',')


            seri = serialization.AccountSerializer(
            query,
            many=True,
            **context
            )

            return seri

        seri = serialization.AccountSerializer(
        query,
        many=True
        )

        return seri

class AccountUpdateView(generics.UpdateAPIView):
    serializer_class = serialization.AccountSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self,*args,**kwargs):
        return self.request.user.account_set.all()

    def get_object(self,*args,**kwargs):
        name = kwargs.get('account_name')
        return self.request.user.account_set.get(name=name)

    def get_serializer(self,*args,**kwargs):
        obj = self.get_object(*args,**kwargs)
        seri = serialization.AccountSerializer(
        obj,
        data=self.request.data,
        context = {'user':self.request.user,'request':self.request}
        )
        return seri


    def put(self,request,*args,**kwargs):

        seri = self.get_serializer(*args,**kwargs)
        if seri.is_valid():
            seri.save()
            return Response(seri.get_initial(),status=status.HTTP_200_OK)

        return Response(seri.errors,status=status.HTTP_400_BAD_REQUEST)

class AccountDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.AccountSerializer

    def get_queryset(self,*args,**kwargs):
        return self.request.user.account_set.all()

    def get_object(self,*args,**kwargs):
        queryset = self.get_queryset(*args,**kwargs)
        acc_name = kwargs.get('account_name')
        return queryset.get(name = acc_name)

    def delete(self,request,*args,**kwargs):
        instance = self.get_object(*args,**kwargs)
        seri = self.serializer_class(instance)
        instance.delete()

        return Response(seri.data,status=status.HTTP_200_OK)



# --------------------Transactions-------------------------

class TransactionView(APIView):
    pass

class TransactionCreateView(generics.CreateAPIView):
    pass

class TransactionUpdateView(generics.UpdateAPIView):
    pass

class TransactionDeleteView(generics.DestroyAPIView):
    pass

class TransactionListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    pagination_class = PageNumberPagination
    serializer_class = serialization.TransactionSerializer
    order_by = '-date'
    paginate_by = 10

    def get_queryset(self,*args,**kwargs):
        acc_name = kwargs.get('account_name')
        try:
            account = self.request.user.account_set.get(name= acc_name)
            return account.transaction_set.all().order_by(self.order_by)
        except django_exceptions.ObjectDoesNotExist :
            pass

    def get(self,request,*args,**kwargs):
        query = self.get_queryset(*args,**kwargs)
        if not query:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(query,many=True)
        return Response(serializer.data)
