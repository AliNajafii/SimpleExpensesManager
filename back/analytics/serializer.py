from rest_framework import serializers
from account import models as account_models
from account.serialization import (
TransactionSerializer
)
from django_restql.mixins import DynamicFieldsMixin


class AccountInfoSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    transaction_number = serializers.IntegerField(
    source='get_transactions_num',
    read_only = True
    )
    expense = serializers.SerializerMethodField(
    'get_expense_transactions',
    read_only = True
    )

    income = serializers.SerializerMethodField(
    'get_income_transactions',
    read_only = True
    )

    last_month_income_avg = serializers.SerializerMethodField(
    'last_month_income_avg',
    read_only = True
    )

    last_month_expense_avg = serializers.SerializerMethodField(
    'last_month_expense_avg',
    read_only = True
    )

    last_time_income_avg = serializers.SerializerMethodField(
    'last_time_income_avg',
    read_only = True
    )

    last_time_expense_avg = serializers.SerializerMethodField(
    'last_time_expense_avg',
    read_only = True
    )

    class Meta:
        model = account_models.Account
        fields = ['transaction_number','last_month_income_avg','last_month_expense_avg','income','expense']

    def get_expense_transactions(self,obj):
        queryset = obj.get_expense_transactions()
        seri = TransactionSerializer(queryset,many=True)
        return seri.data


    def get_income_transactions(self,obj):
        queryset = obj.get_income_transactions()
        seri = TransactionSerializer(queryset,many=True)
        return seri.data


    def last_month_income_avg(self,obj):
        avg = obj.last_month_income_avg()
        return avg.get('inc_avg')


    def last_month_expense_avg(self,obj):
        return obj.last_month_expense_avg().get('exp_avg')

    def last_time_income_avg(self,obj):
        time = self.context.get('time')
        if not time:
            time = {'weeks':1}

        avg = obj.last_time_income_avg(**time)
        return avg

    def last_time_expense_avg(self,obj):
        time = self.context.get('time')
        if not time:
            time = {'weeks':1}

        avg = obj.last_time_expense_avg(**time)
        return avg





class TagInfoSerializer(DynamicFieldsMixin,serializers.ModelSerializer):

    transaction_number = serializers.SerializerMethodField(
    'get_transactions_num',
    read_only = True
    )

    expense = serializers.SerializerMethodField(
    'get_expense_transactions',
    read_only = True
    )

    income = serializers.SerializerMethodField(
    'get_income_transactions',
    read_only = True
    )

    balance = serializers.SerializerMethodField(
    'get_transaction_balance',
    read_only = True
    )

    class Meta:
        model = account_models.Tag
        fields = [
        'balance','income','expense',
        'transaction_number'
        ]

    def get_transactions_num(self,obj):
        return obj.get_transactions_num()


    def get_expense_transactions(self,obj):
        queryset = obj.get_expense_transactions()
        seri = TransactionSerializer(queryset,many=True)
        return seri.data


    def get_income_transactions(self,obj):
        queryset = obj.get_income_transactions()
        seri = TransactionSerializer(queryset,many=True)
        return seri.data

    def get_transaction_balance(self,obj):
        return obj.get_transaction_balance()['balance']


class CategroryInfoSerializer(DynamicFieldsMixin,serializers.ModelSerializer):

    balance = serializers.SerializerMethodField(
    'get_transaction_balance',
    read_only = True
    )

    inc_avg = serializers.SerializerMethodField(
    'get_inc_avg',
    read_only = True
    )

    avg_expense = serializers.SerializerMethodField(
    'get_exp_avg',
    read_only = True
    )

    transaction_number = serializers.SerializerMethodField(
    'get_transactions_num',
    read_only = True
    )

    expense = serializers.SerializerMethodField(
    'get_expense_transactions',
    read_only = True
    )

    income = serializers.SerializerMethodField(
    'get_income_transactions',
    read_only = True
    )

    balance = serializers.SerializerMethodField(
    'get_transaction_balance',
    read_only = True
    )

    class Meta:
        model = account_models.Category

        fields = ['balance','income','expense',
        'transaction_number','inc_avg','avg_expense']

    def get_transaction_balance(self,obj):

        return obj.get_balance_of_transactions().get('balance')

    def get_inc_avg(self,obj):
        return obj.inc_avg().get('inc_avg')

    def get_exp_avg(self,obj):
        return obj.avg_expense().get('exp_avg')

    def get_transactions_num(self,obj):
        return obj.get_transactions_num()


    def get_expense_transactions(self,obj):
        queryset = obj.get_expense_transactions()
        seri = TransactionSerializer(queryset,many=True)
        return seri.data


    def get_income_transactions(self,obj):
        queryset = obj.get_income_transactions()
        seri = TransactionSerializer(queryset,many=True)
        return seri.data
