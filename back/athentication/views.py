from rest_framework_jwt.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser,SAFE_METHODS
from account import serialization
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import exceptions as django_exceptions

class LoginView(APIView):
    pass

class LogoutView(APIView):
    pass

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serialization.UserSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        username = self.kwargs.get('username')
        queryset = self.get_queryset()
        try:
            obj = queryset.get(username=username)
            return obj
        except django_exceptions.ObjectDoesNotExist:
            pass

    def update(self,request,*args,**kwargs):
        obj = self.get_object()
        if obj:
            seri = self.serializer_class(obj,data=request.data)
            if seri.is_valid():
                seri.save()
                return Response(seri.data,status=status.HTTP_200_OK)
            return Response(seri.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
