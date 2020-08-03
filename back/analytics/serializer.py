from rest_framework import serializers
from account import models as account_models
from account.serialization import (
TransactionSerializer
)
from django_restql.mixins import DynamicFieldsMixin
from django_restql.fields import DynamicSerializerMethodField
from account.account_views import URLQueryParamsMixin


class AccountInfoSerializer(DynamicFieldsMixin,
URLQueryParamsMixin,
serializers.ModelSerializer):
    transaction_number = serializers.IntegerField(
    source='get_transactions_num',
    read_only = True
    )
    expense = DynamicSerializerMethodField(

    read_only = True
    )

    income = DynamicSerializerMethodField(

    read_only = True
    )

    last_month_income_avg = DynamicSerializerMethodField(

    read_only = True
    )

    last_month_expense_avg = DynamicSerializerMethodField(

    read_only = True
    )

    last_time_income_avg = DynamicSerializerMethodField(

    read_only = True
    )

    last_time_expense_avg = DynamicSerializerMethodField(

    read_only = True
    )

    last_time_expense_amount = DynamicSerializerMethodField(
    read_only = True
    )

    last_time_income_amount = DynamicSerializerMethodField(
    read_only = True
    )

    class Meta:
        model = account_models.Account
        fields = ['transaction_number',
        'last_month_income_avg',
        'last_month_expense_avg',
        'income',
        'expense',
        'last_time_income_avg',
        'last_time_expense_avg',
        'last_time_expense_amount',
        'last_time_income_amount'
        ]

    def get_last_time_expense_amount(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        amounts_query = obj.last_time_expense_amount_list(**time)
        return {
            'amounts' : list(amounts_query),
            'count': amounts_query.count()
        }

    def get_last_time_income_amount(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        amounts_query = obj.last_time_income_amount_list(**time)
        return {
            'amounts' : list(amounts_query),
            'count': amounts_query.count()
        }

    def get_expense(self,obj,query):
        queryset = obj.get_expense_transactions()
        seri = TransactionSerializer(
            queryset,many=True,
            query=query,
            context = self.context

            )
        return seri.data


    def get_income(self,obj,query):
        queryset = obj.get_income_transactions()
        seri = TransactionSerializer(
            queryset,many=True,
            query=query,
            context = self.context
            )
        return seri.data


    def get_last_month_income_avg(self,obj,query):
        avg = obj.last_month_income_avg()
        return avg.get('inc_avg')


    def get_last_month_expense_avg(self,obj,query):
        return obj.last_month_expense_avg().get('exp_avg')

    def get_last_time_income_avg(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        if not time:
            time = {'weeks':1}

        avg = obj.last_time_income_avg(**time)
        return avg.get('inc_avg')

    def get_last_time_expense_avg(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))

        if not time:
            time = {'weeks':1}

        avg = obj.last_time_expense_avg(**time)
        return avg.get('exp_avg')





class TagInfoSerializer(
    DynamicFieldsMixin,
    URLQueryParamsMixin,
    serializers.ModelSerializer
    ):

    transaction_number = DynamicSerializerMethodField(
    read_only = True
    )

    expense = DynamicSerializerMethodField(

    read_only = True
    )

    income = DynamicSerializerMethodField(

    read_only = True
    )

    balance = DynamicSerializerMethodField(

    read_only = True
    )

    last_time_expense_amount = DynamicSerializerMethodField(
    read_only = True
    )

    last_time_income_amount = DynamicSerializerMethodField(
    read_only = True
    )

    class Meta:
        model = account_models.Tag
        fields = [
        'balance','income','expense',
        'transaction_number',
        'last_time_expense_amount',
        'last_time_income_amount'
        ]

    def get_transaction_number(self,obj,query):
        return obj.get_transactions_num()


    def get_expense(self,obj,query):
        queryset = obj.get_expense_transactions()
        seri = TransactionSerializer(
            queryset,
            many=True,
            query=query,
            context = self.context
            )
        return seri.data


    def get_income(self,obj,query):
        queryset = obj.get_income_transactions()
        seri = TransactionSerializer(
            queryset,
            many=True,
            query=query,
            context = self.context

            )
        return seri.data

    def get_balance(self,obj,query):
        return obj.get_transaction_balance()['balance']

    def get_last_time_expense_amount(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        amounts_query = obj.last_time_expense_amount_list(**time)
        return {
            'amounts' : list(amounts_query),
            'count': amounts_query.count()
        }

    def get_last_time_income_amount(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        amounts_query = obj.last_time_income_amount_list(**time)
        return {
            'amounts' : list(amounts_query),
            'count': amounts_query.count()
        }


class CategroryInfoSerializer(
    DynamicFieldsMixin,
    URLQueryParamsMixin,
    serializers.ModelSerializer):

    balance = DynamicSerializerMethodField(

    read_only = True
    )

    inc_avg = DynamicSerializerMethodField(

    read_only = True
    )

    avg_expense = DynamicSerializerMethodField(

    read_only = True
    )

    transaction_number = DynamicSerializerMethodField(

    read_only = True
    )

    expense = DynamicSerializerMethodField(

    read_only = True
    )

    income = DynamicSerializerMethodField(

    read_only = True
    )


    last_time_expense_amount = DynamicSerializerMethodField(
    read_only = True
    )

    last_time_income_amount = DynamicSerializerMethodField(
    read_only = True
    )


    class Meta:
        model = account_models.Category

        fields = [
        'balance','income','expense',
        'transaction_number',
        'inc_avg',
        'avg_expense',
        'last_time_expense_amount',
        'last_time_income_amount'
        ]

    def get_balance(self,obj,query):

        return obj.get_balance_of_transactions().get('balance')

    def get_inc_avg(self,obj,query):
        return obj.inc_avg().get('inc_avg')

    def get_exp_avg(self,obj,query):
        return obj.avg_expense().get('exp_avg')

    def get_transaction_number(self,obj,query):
        return obj.get_transactions_num()


    def get_expense(self,obj,query):
        queryset = obj.get_expense_transactions()
        seri = TransactionSerializer(
            queryset,many=True,
            query=query,
            context = self.context
            )
        return seri.data


    def get_income(self,obj,query):
        queryset = obj.get_income_transactions()
        seri = TransactionSerializer(
            queryset,many=True,
            query=query,
            context = self.context
            )
        return seri.data

    def get_last_time_expense_amount(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        amounts_query = obj.last_time_expense_amount_list(**time)
        return {
            'amounts' : list(amounts_query),
            'count': amounts_query.count()
        }

    def get_last_time_income_amount(self,obj,query):
        time = self.get_time_from_query(self.context.get('request'))
        amounts_query = obj.last_time_income_amount_list(**time)
        return {
            'amounts' : list(amounts_query),
            'count': amounts_query.count()
        }
