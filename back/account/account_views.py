from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core import exceptions
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
    authentication_classes = (JSONWebTokenAuthentication,)



    def post(self,request,*args,**kwargs):

        seri = serialization.AccountSerializer(data=request.data,
        context={'user':request.user})
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
    authentication_classes = (JSONWebTokenAuthentication,)
    USER = get_user_model()
    renderer_classes = (JSONRenderer,)
    def get(self,request,*args,**kwargs):
        try :
            user = request.user
            account = user.account_set.get(name = kwargs.get('account_name'))
            seri = serialization.AccountSerializer(account,fields=('balance','transaction_set',),context={'transaction_fields':('amount',)})
            res = Response(data= seri.data,status=status.HTTP_200_OK)

            return res
        except exceptions.ObjectDoesNotExist :
            return Response(
            data={'error':'username or account  not found.'},
            status= status.HTTP_400_BAD_REQUEST
            )

    def http_method_not_allowed(self,request,*args,**kwargs):
        if not request.method == 'GET':
            raise MethodNotAllowed(method=request.method)

class queryparams(APIView):
    def get(self,request,*args,**kwargs):
        return Response(
        {
        'params': request.query_params
        }
        )
class UserAccountListView(generics.ListAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)

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
    pass

class AccountDeleteView(generics.DestroyAPIView):
    pass

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
    pass
