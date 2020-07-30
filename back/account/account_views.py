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
    time_fileds = ['year','month','week','days']

    def get_fields_from_query(self,request):
        fields = self.request.query_params.get(self.fields_query_kwarg)
        if fields:
            fields = f',{fields}'.split(',') # for avoiding none functionality
            return tuple(fields)

    def get_time_from_query(self,request):
        qp = request.query_params
        time_params = {}
        for time in self.time_fileds:
            time_params.update({time:qp.get('time')})

        return time_params



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

class AccountProfileView(APIView,URLQueryParamsMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    USER = get_user_model()
    renderer_classes = (JSONRenderer,)
    def get(self,request,*args,**kwargs):
        try :
            user = request.user
            account = user.account_set.get(name = kwargs.get('account_name'))
            fields = self.get_fields_from_query(request)
            seri = serialization.AccountSerializer(account,fields=fields)

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

class UserAccountListView(generics.ListAPIView,URLQueryParamsMixin):

    authentication_classes = (BasicAuthentication,)

    def get_queryset(self,*args,**kwargs):
        return self.request.user.account_set.all()

    def get_serializer(self,*args,**kwargs):
        # client can choose the field for json representation
        seri = None
        query = self.get_queryset()
        fields = self.get_fields_from_query(self.request)
        seri = serialization.AccountSerializer(
                query,
                many=True,
                fields = fields
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

class TransactionView(APIView,URLQueryParamsMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.TransactionSerializer

    def get_serializer(self,*args,**kwargs):
        fields = self.get_fields_from_query(self.request)
        if self.serializer_class:
            return self.serializer_class(fields=fields,*args,**kwargs)
        return serialization.TransactionSerializer(fields=fileds,*args,**kwargs)

    def get_queryset(self,*args,**kwargs):
            acc_name = kwargs.get('account_name')
            try:
                accounts = self.request.user.account_set.get(name=acc_name)
                transactions = accounts.transaction_set.all()
                return transactions
            except django_exceptions.ObjectDoesNotExist:
                pass

    def get_object(self,*args,**kwargs):
        id = kwargs.get('transaction_id')
        query = self.get_queryset(*args,**kwargs)
        if query :
            try:
                obj = query.get(id=id)
                return obj
            except django_exceptions.ObjectDoesNotExist:
                pass

    def get(self,request,*args,**kwargs):

        obj = self.get_object(*args,**kwargs)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serilizer = self.get_serializer(obj)
        return Response(serilizer.data,status=status.HTTP_200_OK)


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = serialization.TransactionSerializer

    def get_queryset(self,*args,**kwargs):
        name = kwargs.get('account_name')
        try:
            account = self.request.user.account_set.get()
            return account.transaction_set.all().order_by('-date')
        except django_exceptions.ObjectDoesNotExist:
            pass


class TransactionUpdateView(generics.UpdateAPIView):
    pass

class TransactionDeleteView(generics.DestroyAPIView):
    pass

class TransactionListView(generics.ListAPIView,URLQueryParamsMixin):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.TransactionSerializer
    pagination_class = LimitOffsetPagination
    # page_size = 1
    # page_query_param = 'page'
    # page_size_query_param = 'page_size'
    order_by = '-date'

    def get_queryset(self,*args,**kwargs):
        acc_name = kwargs.get('account_name')
        try:
            account = self.request.user.account_set.get(name= acc_name)
            return account.transaction_set.all().order_by(self.order_by)
        except django_exceptions.ObjectDoesNotExist :
            pass
    def get_serializer(self,*args,**kwargs):
        fields = self.get_fields_from_query(self.request)
        cls = self.serializer_class
        query = self.get_queryset(*args,**kwargs)
        return cls(query,fields=fields,many=True)

    def get(self,request,*args,**kwargs):
        serializer = self.get_serializer(*args,**kwargs)
        return Response(serializer.data)
