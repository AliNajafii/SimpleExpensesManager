from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action

class AccountViewSet(ModelViewSet):
    lookup_field = 'pk'
    authentication_classes = (BasicAuthentication,)

    # @action(methods = ['GET'])
