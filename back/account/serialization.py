from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import copy
from . import models


class URLField(serializers.RelatedField):

    def to_representation(self,value):
        return {
        'url':value.get_absolute_url()
        }



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        self.name = kwargs.pop('name',None) #for specification of selected fields for child serializers
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
        # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)



class CategorySerializer(DynamicFieldsModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    class Meta:
        model = models.Category
        exclude = ('id',)
        read_only_fields = ('date',)

class TagSerializer(DynamicFieldsModelSerializer):
        url = serializers.CharField(source='get_absolute_url')
        class Meta:
            model = models.Tag
            exclude = ('id',)
            read_only_fields = ('date',)

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta():
        model = get_user_model()
        fields = ('username','first_name','last_name','email',)
        write_only_fields = ('password',)
        extra_kwargs = {
        'password':{
            'required':True
        }
        }

class TransactionSerializer(DynamicFieldsModelSerializer):
    tag = TagSerializer(fields=('url',),many=True,required=False)
    category = CategorySerializer(fields=('url',),required=False)
    url = serializers.SerializerMethodField('get_transaction_url')

    def get_transaction_url(self,obj):
        return obj.get_absolute_url()

    class Meta():
        model = models.Transaction
        fields=('url','is_expense','amount','date','note','tag','category')
        read_only_fields = ('date',)
        extra_kwargs = {
            'category':{
                'required':False
            },
            'note':{
                'required' :False
            },
        }

    def create(self,validated_data):
        tag = validated_data.get('tag')
        category = validated_data.get('category')

        tags = validated_data.pop('tag') if tag  is not None  else []
        cat = validated_data.pop('category') if category is not None  else category
        tag_list = []
        if tags:
            for tag in tags:
                t = models.Tag.objects.create(**tag)
                tag_list.append(t)
        if category:
            category = models.Category.objects.create(**cat)
        instance = models.Transaction(
        category = category,
        **validated_data
        )
        if tags:
            instance.tag.add(*tag_list)
        if category:
            instance.category = category
        instance.save(operate_on=True)
        return instance

    def update(self,instance,validated_data):

        tags = validated_data.get('tag')
        tag_list = []

        if tags :
            for tag in tags:
                t = models.Tag.objects.get_or_create(**tag)
                tag_list.append(t)
            instance.tag.add(*tag_list)

        instance.category = validated_data.get('category',instance.category)

        amount = validated_data.get('amount')
        # check if amount of transaction is changed then oprate on account total.
        # if amount is equal as older amount it should not oprate on account balance.
        operate_on = False
        if amount and amount != instance.amount:
            operate_on =True
            instance.amount = amount
        instance.is_expense = validated_data.get('is_expense',instance.is_expense)
        instance.note = validated_data.get('note',instance.note)
        instance.save(operate_on)
        return instance

class AccountSerializer(DynamicFieldsModelSerializer):
    transaction_set = TransactionSerializer(name='transaction',many=True,required=False)
    user = UserSerializer(name='user',read_only =True)
    class Meta():
        model = models.Account
        exclude = ('id',)
        read_only_fields = ('date','user','balance',)
        extra_kwargs = {
        'name':{'required':False},
        }


    def validate_name(self,value):
        """
        this method is for check name ,
        for uniqe in the creation not update.
        """
        if self.context.get('test'):
            return value
        if len(value) > 1000 :
            serializers.ValidationError(
            detail='Account name characters could not be more than 1000.'
            )

        if self.context.get('request').method == 'POST' :
            if not value :
                raise serializers.ValidationError(
                detail='Account name is required.'
                )
            user = self.context.get('user')
            if not user :
                raise ValueError('user should pass by context keyword')
            try :
                ins = user.account_set.get(name=value)
                raise serializers.ValidationError(
                detail='This name for account has been used.'
                )
            except ObjectDoesNotExist :
                pass

        return value


    def create(self,validated_data):

        account = self.Meta.model.objects.create(
        user = self.context.pop('user'),
        **validated_data
        )
        return account

    def update(self,instance,validated_data):

        instance.total = validated_data.get('total',instance.total)
        instance.name = validated_data.get('name',instance.name)
        instance.update_balance(save=False)
        instance.save()
        return instance
