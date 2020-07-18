from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core import exceptions
from rest_framework.response import Response
from rest_framework import status
from . import serialization
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes

class AccountCreateView(generics.CreateAPIView):
    pass


class AccountProfileView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication,)
    USER = get_user_model()
    renderer_classes = (JSONRenderer,)
    def get(self,request,*args,**kwargs):
        try :
            user = self.USER.objects.get(username = kwargs.get('username'))
            account = user.account_set.get(name = kwargs.get('account_name'))
            seri = serialization.AccountSerializer(account)
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


class AccountListView(generics.ListAPIView):
    pass

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
