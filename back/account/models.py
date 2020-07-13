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
    'Tag',
    null=True
    )
    category = models.ForeignKey(
    'Category',
    on_delete=models.CASCADE,
    null=True
    )

    def __str__(self):
        if self.is_expense:
            return f"-{self.amount} from {self.account.name}"

        return f"+{self.amount} from {self.account.name}"


    def tag_number(self):
        return self.tag_set.all().count()

    def get_user(self,obj=True):
        """
        this method return username,email,first,last
        of a transaction.
        if obj True user instance will be return else
        dictionary of info.
        """
        user = self.account.user
        if obj:
            return user

        info = {}
        info.update({
        'username' : user.username,
        'email': user.email,
        'full_name': user.get_full_name()
                })

class Category(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

    def get_transactions_num(self):
        return self.transaction_set.all().count()

    def get_expense_transactions(self):
        return self.transaction_set.filter(is_expense =True)

    def get_income_transactions(self):
        return self.transaction_set.filter(is_expense=False)

    def get_balance_of_transactions(self):
        """
        this method get the balance amount,
         of income and expense of a specific category.
        """

        incs = models.Sum('amount',filter=models.Q(is_expense=False))
        exps = models.Sum('amoutn',filter=models.Q(is_expense=True))

        balance = self.transaction_set.aggregate(balance= incs - exps)

        return balance



class Tag(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    def __str__(self):
        return f"{self.name}"

    def get_transaction_number(self):
        return self.transaction_set.aggregate(num=models.count('transaction_set'))

    def get_expense_transaction(self):

        return self.transaction_set.filter(is_expense=True)

    def get_income_transaction(self):

        return self.transaction_set.filter(is_expense=False)

    def get_transaction_balance(self):

        incs = models.Sum('amount',filter=models.Q(is_expens=False))
        exps = models.Sum('amount',filter=models.Q(is_expens=True))

        balance = self.transaction_set.aggregate(
        balance = incs - exps
        )

        return balance


class TransactionNotValid(Exception):
    def __init__(self,*args):
        super().__init__(*args)
