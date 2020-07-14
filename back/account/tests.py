from django.test import TestCase
from . import models
from django.contrib.auth.models import User
from django.db.models import Sum,Q
class GeneralTest(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(
        username='alal',
        email='ali@najafi.com',
        first_name= 'Ali',
        last_name = 'Najafi'
        )

    def create_cat(self,num):
        lst =[]
        for i in range(num):
            obj = models.Category.objects.create(
            name = f'cat{i}'
            )
            lst.append(obj)
        return lst

    def create_tag(self,num,transactions=0):
        lst=[]
        for i in range(num):
            obj = models.Tag.objects.create(
            name=f'tag{1}'
            )
            lst.append(obj)
        return lst

    def create_trans(self,num,account=None,amount=100,is_expense=True,tag=0,cat=0):
        lst=[]
        if not account:
            account = self.acc1
        for i in range(num):
            obj = models.Transaction.objects.create(
            account = account,
            amount = amount,
            note=f'note{i}',
            is_expense=is_expense
            )

            if tag:
                instances = self.create_tag(tag)
                obj.tag.add(*instances)
            if cat:
                if cat >=1:
                    category = self.create_cat(1)[0]
                    obj.category = category
            lst.append(obj)
        return  lst

    def create_account(self,num,total=1000,balance=0):
        lst=[]
        for i in range(num):
            obj = models.Account.objects.create(
            name=f'acc{i}',
            user=self.u1,
            total=total,
            balance=balance
            )
            lst.append(obj)

        return lst

    def create_user(self,num):
        lst = []
        for i in range(num):
            obj = User.objects.create_user(
            username=f'username_{1}',
            first_name = f'first_{1}',
            last_name = f'last_{1}',
            email=f'email_{1}@email.com'
            )
            lst.append(obj)
        return lst

    def test_transaction(self):
        ac1 = models.Account.objects.create(
        user=self.u1,
        name='acc2',
        total=1000
        )
        t1 = models.Transaction(
        account = ac1,
        amount = 100,
        note='note1'
        )
        t2 = models.Transaction(
        account = ac1,
        amount = 200,
        note='note2',
        is_expense=False
        )
        # testing account satatics
        self.assertEqual(ac1.total,1000)
        self.assertEqual(ac1.balance,0)
        #test t1 transaction statics
        self.assertEqual(t1.amount,100)
        self.assertTrue(t1.is_expense,True)
        self.assertIsNone(t1.category)
        self.assertEqual(t1.__str__(),'-100 from acc2')

        self.assertEqual(t2.__str__(),'+200 from acc2')
        #testing account statics after transaction save method
        # -100 transaction added
        t1.save()
        self.assertEqual(ac1.total,900)
        self.assertIn(t1,ac1.transaction_set.all())
        # +200 transaction added
        t2.save()
        self.assertEqual(ac1.total,1100)
        self.assertIn(t1,ac1.transaction_set.all())

    def test_account(self):
        #before transactions
        acc1 = self.create_account(1)[0]
        self.assertEqual(acc1.total,1000)
        self.assertEqual(acc1.balance,0)
        #after transactions
        # -100 expense added
        expss = self.create_trans(1,acc1,100)
        #2 * +200 transaction added
        incs = self.create_trans(2,acc1,200,False)


        self.assertEqual(acc1.total,1300)

        #check for expense transaction quantitiy
        self.assertEqual(
        acc1.transaction_set.filter(is_expense=True).count(),
        len(expss)
        )
        #check for income transaction quantity
        self.assertEqual(
        acc1.transaction_set.filter(is_expense=False).count(),
        len(incs)
        )
        
        #check balance
        acc1.update_balance()
        self.assertEqual(acc1.balance,300)
