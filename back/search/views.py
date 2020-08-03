from django.shortcuts import render
from .serializers import SearchSerializer
from rest_framework.response import Response
from rest_framework import status
from account.serialization import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from account.paginators import DefaultPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics
from account.models import Transaction
from django.db.models import Prefetch
from django.db.models import Q

class SearchAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    pagination_class = DefaultPagination
    serializer_class = SearchSerializer
    result_serializer_class = TransactionSerializer

    def get_queryset(self,query_fields=None):
        trans1 = Transaction.objects.select_related('category')
        trans2 = Transaction.objects.prefetch_related('tag')
        empty_query = Transaction.objects.none() #empty queryset for union trans1 and trans 2
        trans_queryset = trans1 & trans2
        trans_queryset = trans_queryset.filter(*query_fields)
        accounts = self.request.user.account_set.prefetch_related(
        Prefetch('transaction_set',queryset= trans_queryset)
        )
        transactions_list = [a.transaction_set.all() for a in accounts]
        transactions = empty_query.union(*transactions_list)
        self.queryset = transactions
        return self.queryset

    def get_serializer(self,*args,**kwargs):

        return self.result_serializer_class(
        context={'request':self.request},
        *args,
        **kwargs
        )

    def list(self,request,*args,**kwargs):
        seri = self.serializer_class(data=self.request.data)
        if seri.is_valid():
            qs = self.process_filter(seri.data)
            queryset = self.get_queryset(qs)
            p_query = self.paginate_queryset(queryset)
            trans_seri = self.get_serializer(p_query,many=True)
            return self.get_paginated_response(trans_seri.data)

        return Response(seri.errors,status=status.HTTP_400_BAD_REQUEST)


    def process_filter(self,data):
        """
        this method processes the filters
        and returns the appropriate django Q
        filters in list format.
        """
        filter = data['filter']
        keyword = data['keyword']
        Qs = []
        tags_kw = Q(tag__name__icontains=keyword)
        cats_kw = Q(category__name__icontains = keyword)
        trans_note_kw = Q(note__icontains = keyword)
        all = tags_kw | cats_kw | trans_note_kw

        if filter['all']:
            Qs.append(all)

        elif filter['tags']:
            Qs.append(tags_kw)

        elif filter['category']:
            Qs.append(cats_kw)

        else :
            Qs.append(trans_note_kw)

        return Qs






# Create your views here.
