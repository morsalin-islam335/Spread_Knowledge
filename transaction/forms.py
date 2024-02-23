from django import forms

from . models import Transaction
from django.contrib.auth.models import User

class TransactionFrom(forms.Form):
    amount = forms.IntegerField()
    
