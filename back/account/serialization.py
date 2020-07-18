from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = get_user_model()
        fields = ('username','first_name','last_name','email',)
        write_only = ('password',)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Transaction
        fields=('is_expense','amount','date','note',)

class TransactionsRelatedField(serializers.RelatedField):
    def to_representation(self,value):
        seri = TransactionSerializer(value)
        return seri.data
    def get_queryset(self):
        return models.Transaction.objects.all()

class AccountSerializer(serializers.ModelSerializer):
    transaction_set = TransactionSerializer(many=True)
    user = UserSerializer()
    class Meta():
        model = models.Account
        exclude = ('id',)
