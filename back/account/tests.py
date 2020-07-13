from django.test import TestCase
from . import models
from django.contrib.auth.models import User
class GeneralTest(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(
        username='alal',
        email='ali@najafi.com',
        first_name= 'Ali',
        last_name = 'Najafi'
        )
        self.acc1 = models.Account.objects.create(
            user=self.u1,
            name='my_acc1',
            total=1000
        )
        self.test_trans = models.Transaction.objects.create(
        amount = 200,
        account=self.acc1
        )

        self.test_cat = models.Category.objects.create(
        name='cat1'
        )

        self.test_tag = models.Tag.objects.create(
        name='tag1'
        )

    def tearDown(self):
        self.acc1.total = 1000

    def create_cat(self,num):
        lst =[]
        for i in range(num):
            obj = models.Category.objects.create(
            name = f'cat{i}'
            )
            lst.append(obj)
        return lst


    def test_transaction_cost(self):
        trans1 = models.Transaction.objects.create(
        amount = 200,
        account=self.acc1
        )

        self.acc1.add_transaction(trans1)
        self.assertEqual(self.acc1.total,800)

    def test_transaction_income(self):
        trans1 = models.Transaction.objects.create(
        amount = 200,
        account=self.acc1
        )

        self.acc1.add_transaction(trans1)
        self.assertEqual(self.acc1.total,1200)

    
