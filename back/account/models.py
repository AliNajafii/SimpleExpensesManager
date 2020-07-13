from django.db import models
from django.contrib.auth import get_user_model
USER = get_user_model()

class Account(models.Model):
    name = models.CharField(max_length=1000)
    total = models.FloatField(default=0)
    balance = models.FloatField(default=0,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
    USER,
    on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Account({self.balance})'

    def add_transaction(self,trans_obj):
        """
        this method gives a Transaction obj
        and calculates the transaction operation,
        on total account cash base on expense or income.
        """
        if trans_obj.account == self:
            if trans_obj.is_expense :
                self.total -= trans_obj.amount
            else:
                self.total += trans_obj.amount
            self.save()
        else:
            raise TransactionNotValid()

    def update_balance(self):
        expenses = models.Sum(
        'amount',
        filter=models.Q(is_expense=True)
        )

        incomes = models.Sum(
        'amount',
        filter = models.Q(is_expense = False)
        )

        balance = self.transaction_set.aggregate(
        value = incomes - expenses
        )

        self.balance = balance.get('value')
        self.save()


class Transaction(models.Model):
    transaction_type = ('exp','inc',)
    is_expense = models.BooleanField(default=True) # if false it is income.
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    note = models.CharField(
    max_length=1000,
    null=True,
    blank = True
    )
    account = models.ForeignKey(
    'Account',
    on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
    'Tag'
    )



class Category(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    transaction = models.ForeignKey(
    'Transaction',
    on_delete = models.CASCADE
    )

class Tag(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)

class TransactionNotValid(Exception):
    def __init__(self,*args):
        super().__init__(*args)
