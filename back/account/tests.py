from django.test import TestCase
from . import models
from django.contrib.auth.models import User
from django.db.models import Sum,Q
class ModelsTest(TestCase):

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

    def create_tag(self,num,transactions=None):
        lst=[]
        for i in range(num):
            obj = models.Tag.objects.create(
            name=f'tag{1}'
            )
            if transactions:
                obj.transaction_set.add(*transactions)
            obj.save()
            lst.append(obj)
        return lst

    def create_trans(self,num,account=None,amount=100,is_expense=True,tag=0,cat=0,operate_on=True):
        lst=[]
        for i in range(num):
            obj = models.Transaction(
            account = account,
            amount = amount,
            note=f'note{i}',
            is_expense=is_expense,

            )

            if tag:
                instances = self.create_tag(tag)
                obj.tag.add(*instances)
            if cat:
                if cat >=1:
                    category = self.create_cat(1)[0]
                    obj.category = category

            obj.save(operate_on=operate_on)
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
        t1.save(operate_on=True)
        self.assertEqual(ac1.total,900)
        self.assertIn(t1,ac1.transaction_set.all())
        # +200 transaction added
        t2.save(operate_on=True)
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
        acc1.update_balance()
        self.assertEqual(acc1.balance,-100)
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

    def test_category(self):
        cat1 = self.create_cat(1)[0]
        acc1 = self.create_account(1)[0]
        exp_transe = []
        exp_transe += self.create_trans(3,acc1)
        inc_transe = []
        inc_transe += self.create_trans(2,acc1,is_expense=False)

        # #add expense transaction only
        for t in exp_transe:
            t.category = cat1
            t.save()

        self.assertEqual(cat1.transaction_set.count(),3)
        self.assertEqual(cat1.get_transactions_num(),3)
        self.assertEqual(
        cat1.get_balance_of_transactions(),
        {'balance':-300}
        )

        #add income transactions too
        for t in inc_transe:
            t.category = cat1
            t.save()

        self.assertEqual(cat1.transaction_set.count(),5)
        self.assertEqual(cat1.get_transactions_num(),5)
        self.assertEqual(cat1.transaction_set.filter(is_expense=False).count(),2)
        self.assertEqual(
        cat1.get_balance_of_transactions(),
        {'balance':-100}
        )


        test_t = models.Transaction.objects.get(id='3')
        self.assertIn(test_t,cat1.transaction_set.all())

    def test_tag(self):
        acc = self.create_account(1)[0]
        transactions= []
        incs = self.create_trans(4,acc,is_expense=False)
        exp = self.create_trans(2,acc)
        transactions += incs
        # insert income transactions first
        tag = self.create_tag(1,transactions)[0]

        self.assertEqual(
        tag.get_transaction_balance(),{'balance':400}
        )

        self.assertEqual(tag.get_transactions_num(),4)

        #adding expense too
        tag.transaction_set.add(*exp)
        tag.save()

        self.assertEqual(tag.get_transactions_num(),6)

        self.assertEqual(
        tag.get_transaction_balance(),
        {'balance':200}
        )

        self.assertTrue(
        tag.get_income_transactions().count()==4 and \
        tag.get_expense_transactions().count()==2
        )
