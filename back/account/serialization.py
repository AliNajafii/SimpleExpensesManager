from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_restql.mixins import DynamicFieldsMixin
from django_restql.fields import DynamicSerializerMethodField
import copy
from . import models


def Update(instance,vali_data):
    """
    this method updates instance with validated_data
    for simpling the process of updating instance in serializers
    """

    attrs = [i for i in vali_data.items()]
    for field,value in attrs:
        if value != getattr(instance,field): # if the value is the same as instance.field value.
            setattr(instance,field,value)
    return instance



# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """

#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)
#         self.name = kwargs.pop('name',None) #for specification of selected fields for child serializers
#         # Instantiate the superclass normally
#         super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
#         if fields is not None:
#         # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)



class CategorySerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url',read_only=True)
    class Meta:
        model = models.Category
        exclude = ('id',)
        read_only_fields = ('date','url',)

    def get_url(self,obj):
        return obj.get_absolute_url()

    def get_queryset(self):
        user = self.context.get('request').user
        return self.Meta.model.objects.filter(user=user)

    def validate_name(self,value):
        if not self.context.get('is_making_transaction'):
    
            queryset = self.get_queryset()
            try :
                used_cat_name = queryset.get(name=value)
                raise serializers.ValidationError(
                detail='This category name has been used.'
                )
            except ObjectDoesNotExist:
                pass
            return value
        return value

    def create(self,validated_data):
        name = validated_data.get('name')
        user = self.context.get('request').user
        instance = self.Meta.model.objects.create(
        name=name,
        user=user
        )
        return instance

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.save()
        return instance

class TagSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
        url = serializers.SerializerMethodField('get_url',read_only=True)
        class Meta:
            model = models.Tag
            exclude = ('id',)
            read_only_fields = ('date',)

        def get_url(self,obj):
            return obj.get_absolute_url()


        def get_queryset(self,*args,**kwargs):
            user = self.context.get('request').user
            return self.Meta.model.objects.filter(user=user)

        def validate_name(self,value):
            if not self.context.get('is_making_transaction'):
                query = self.get_queryset()
                used_tag_name = None
                try :
                    used_tag_name = query.get(name=value)
                    raise serializers.ValidationError(detail='this tag name was used.')
                except ObjectDoesNotExist :
                    pass

                return value
            return value

        def create(self,validated_data):
            user = self.context.get('request').user
            name = validated_data.get('name')
            instance = self.Meta.model.objects.create(
            user=user,
            name=name
            )
            return instance

        def update(self,instance,validated_data):
            instance.name = validated_data.get('name',instance.name)
            instance.save()
            return instance

class UserSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    class Meta():
        model = get_user_model()
        fields = ('username',
        'first_name',
        'last_name',
        'email',
        'password',
        'date_joined',
        'last_login',

        )
        extra_kwargs = {
        'password':{
            'required':True,
            'write_only':True
        },
        'date_joined':{
            'read_only':True
        },

        'last_login':{
            'read_only':True
        }
        }

        def create(self,validate_data):
            user = self.model.objects.create_user(**validate_data)
            return user

        def update(self,instance,validate_data):
            # passsword = None
            # if validate_data.get('password'):
            #     password = validate_data.pop('password')
            # obj= Update(instance,validate_data)
            # if password:
            #     obj.set_password(password)
            # obj.save()
            # return obj

            dfsddsg
            

class TransactionSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    tag = TagSerializer(many=True,required=False)
    category = CategorySerializer(required=False)
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
    
    def validate(self,attrs):
        account = self.context.get('account')
        if attrs.get('is_expense'):
            if account.total < attrs.get('amount'):
                raise serializers.ValidationError(
                    detail='Transaction Amount is bigger than account total'
                )
        if attrs.get('tag'):
            tags = TagSerializer(
                data=attrs.get('tag'),
                many=True,
                context=self.context
                )
            if not tags.is_valid():
                raise serializers.ValidationError(
            detail= tags.errors
            )

        if attrs.get('category'):
            cat_seri = CategorySerializer(data=attrs.get('category'),context=self.context)
            if not cat_seri.is_valid():
                raise serializers.ValidationError(
            detail= cat_seri.errors
            )
        
        return super().validate(attrs)

    def create(self,validated_data):
        tag = validated_data.get('tag')
        category = validated_data.get('category')
        account = self.context.get('account')

        tags = validated_data.pop('tag') if tag  is not None  else []
        cat = validated_data.pop('category') if category is not None  else category
        tag_list = []
        user = self.context.get('request').user
        instance = models.Transaction(
        account = account,
        **validated_data
        )
        instance.save(operate_on=True)
        if tags:
            for tag in tags:
                t = models.Tag.objects.get_or_create(user=user,**tag)[0]
                tag_list.append(t)
            instance.tag.add(*tag_list)

        if category:
            category = models.Category.objects.get_or_create(user=user,**cat)[0]
            instance.category = category

        
        return instance

    def update(self,instance,validated_data):

        
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

class AccountSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    transaction_set = TransactionSerializer(many=True,required=False)
    user = UserSerializer(read_only =True)
    class Meta():
        model = models.Account
        exclude = ('id',)
        read_only_fields = ('date','user','balance',)
        extra_kwargs = {
        'user':{'required':False,'read_only':True},
        }


    def validate_name(self,value):
        """
        this method is for check name ,
        for uniqe in the creation not update.
        """


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
