from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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

    def get_absolute_url(self):
        return reverse(
        'account_profile',
        kwargs={
        'username':self.user.username,
        'account_name':self.name
        })

    def __str__(self):
        return f'Account({self.total})'

    def add_transaction(self,trans_obj):
        """
        this method gives a Transaction obj
        and calculates the transaction operation,
        on total account cash base on expense or income.
        """
        if trans_obj.account == self:
            if trans_obj.is_expense :
                self.total -= trans_obj.amount
                if self.total < 0 :
                    raise ValidationError(message=_('The cost amount is bigger than the total account cash. '))

            else:
                self.total += trans_obj.amount
            self.update_balance(save=False)
            self.save()
        else:
            raise TransactionNotValid()

    def update_balance(self,save=True):
        incs = 0
        exps = 0
        if self.get_income_transactions().exists():
            incs = models.Sum('amount',filter=models.Q(is_expense=False))
        if self.get_expense_transactions().exists():
            exps = models.Sum('amount',filter=models.Q(is_expense=True))
        else :
            return None
        balance= self.transaction_set.aggregate(balance= incs - exps)

        self.balance = balance.get('balance')
        if save:
            self.save()

    def get_transactions_num(self):
        return self.transaction_set.all().count()

    def get_expense_transactions(self):
        return self.transaction_set.filter(is_expense =True)

    def get_income_transactions(self):
        return self.transaction_set.filter(is_expense=False)


    def last_month_income_avg(self):
        """
            this method return the average of,
            last month income transactions.
        """
        d1 = timezone.now()
        d2 = d1 - relativedelta(months=1)
        avg_income = models.Avg(
        'amount',
        filter= models.Q(date__range=(d2,d1),is_expense=False)
        )
        avg = self.transaction_set.aggregate(inc_avg = avg_income)

        return avg


    def last_time_income_avg(self,number_of_duration,*args,**kwargs):
        """
        this method return the average of last,
        month,week and/or hour income transactions.
        note : one of those three time parameters could be True.

        """
        number = number_of_duration or \
        kwargs.get('number_of_duration')

        d1 = timezone.now()
        d2 = None
        if kwargs.get('months'):
            d2 = d1 - relativedelta(months=number)
        elif kwargs.get('weeks'):
            d2 = d1 - relativedelta(weeks = number)
        elif kwargs.get('days') :
            d2 = d1 - relativedelta(days=number)

        avg_income = models.Avg(
        'amount',
        filter= models.Q(date__range=(d2,d1),is_expense=False)
        )

        avg = self.transaction_set.aggregate(inc_avg = avg_income)

        return avg


    def last_month_expense_avg(self):
            """
                this method return the average of,
                last month income transactions.
            """
            d1 = timezone.now()
            d2 = d1 - relativedelta(months=1)
            avg_income = models.Avg(
            'amount',
            filter= models.Q(date__range=(d2,d1),is_expense=True)
            )
            avg = self.transaction_set.aggregate(exp_avg = avg_income)

            return avg


    def last_time_expense_avg(self,number_of_duration,*args,**kwargs):
            """
            this method return the average of last,
            month,week and/or hour income transactions.
            note : one of those three time parameters could be True.

            """
            number = number_of_duration or \
            kwargs.get('number_of_duration')

            d1 = timezone.now()
            d2 = None
            if kwargs.get('months'):
                d2 = d1 - relativedelta(months=number)
            elif kwargs.get('weeks'):
                d2 = d1 - relativedelta(weeks = number)
            elif kwargs.get('days') :
                d2 = d1 - relativedelta(days=number)

            avg_income = models.Avg(
            'amount',
            filter= models.Q(date__range=(d2,d1),is_expense=True)
            )

            avg = self.transaction_set.aggregate(exp_avg = avg_income)

            return avg



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

    def get_absolute_url(self):
        return reverse(
        'transaction_detail',
        kwargs={
        'username':self.account.user.username,
        'account_name':self.account.name,
        }
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

        return info

    def save(self,operate_on=False,*args,**kwargs):
        if operate_on or kwargs.get('operate_on'):
            self.account.add_transaction(self)
        super().save(*args,**kwargs)



class Category(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
    USER,
    on_delete=models.CASCADE,
    default = None,
    null=True
    )
    def get_absolute_url(self):
        return reverse(
        'category_detail',

        )
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
        incs = 0
        exps = 0
        if self.get_income_transactions().exists():
            incs = models.Sum('amount',filter=models.Q(is_expense=False))
        if self.get_expense_transactions().exists():
            exps = models.Sum('amount',filter=models.Q(is_expense=True))
        balance= self.transaction_set.aggregate(balance= incs - exps)

        return balance
    def inc_avg(self,**duration):
        """
        this method is for calculating the average of
        income in this category.
        **duration kwargs are : {'month':duration},
        {'week':duration},{'day':duration}
        note = if **duration is None {'month':1} will be
        calculated. and one of them should be choosen .
        """
        duraton_info = {}
        now = timezone.now()
        past = None
        if duration:
            if duration.keys()[0] == 'month':

                past = now - relativedelta(months=duration.get('month'))

            elif duration.keys()[0] == 'week':
                past = now - relativedelta(weeks=duration.get('week'))

            elif duration.keys()[0] == 'day':
                past = now - relativedelta(days=duration.get('day'))
            else : # if **duration was not None but wrong kwargs had given
                past = now - relativedelta(months=1)
        else : # id **duration was None
            past = now - relativedelta(months=1)


        avg = models.Avg(
        'amount',
        filter= models.Q(date__range=(now-past,now),is_expense=False)

        )

        return self.transaction_set.aggregate(inc_avg = avg)


    def avg_expense(self,**duration):

        """
        this method is for calculating the average of
        income in this category.
        **duration kwargs are : {'month':duration},
        {'week':duration},{'day':duration}
        note = if **duration is None {'month':1} will be
        calculated. and one of them should be choosen .
        """
        duraton_info = {}
        now = timezone.now()
        past = None
        if duration:
            if duration.keys()[0] == 'month':

                past = now - relativedelta(months=duration.get('month'))

            elif duration.keys()[0] == 'week':
                past = now - relativedelta(weeks=duration.get('week'))

            elif duration.keys()[0] == 'day':
                past = now - relativedelta(days=duration.get('day'))
            else : # if **duration was not None but wrong kwargs had given
                past = now - relativedelta(months=1)
        else : # id **duration was None
            past = now - relativedelta(months=1)


        avg = models.Avg(
        'amount',
        filter= models.Q(date__range=(now-past,now),is_expense=True)

        )

        return self.transaction_set.aggregate(exp_avg = avg)


class Tag(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(
    USER,
    on_delete=models.CASCADE,
    default = None,
    null=True
    )
    def __str__(self):
        return f"{self.name}"

    def get_transactions_num(self):
        return self.transaction_set.count()

    def get_expense_transactions(self):

        return self.transaction_set.filter(is_expense=True)

    def get_income_transactions(self):

        return self.transaction_set.filter(is_expense=False)

    def get_transaction_balance(self):

        incs = 0
        exps = 0
        if self.get_income_transactions().exists():
            incs = models.Sum('amount',filter=models.Q(is_expense=False))
        if self.get_expense_transactions().exists():
            exps = models.Sum('amount',filter=models.Q(is_expense=True))
        balance= self.transaction_set.aggregate(balance= incs - exps)

        return balance


class TransactionNotValid(Exception):
    def __init__(self,*args):
        super().__init__(*args)
