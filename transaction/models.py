from django.db import models
from account . models import Account
from book.models import Borrow

# Create your models here.

class Transaction(models.Model):
    amount = models.IntegerField()
    balance_after_transaction = models.IntegerField()
    account = models.ForeignKey(Account, on_delete = models.CASCADE, null = True, blank = True) # an user may have multiple transaction
    borrow = models.OneToOneField(Borrow, on_delete = models.CASCADE, null = True, blank = True, related_name = 'borrowTransaction') # a borrow have at most 1 transaction


    def  __str__(self):
        return f"Name : {self.account.user.first_name} {self.account.user.last_name} Amount : {self.amount}"

