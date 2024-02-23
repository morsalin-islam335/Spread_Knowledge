from django.urls import path 


from . views import DepositMoneyTransaction


urlpatterns = [
    path("depositMoney/", DepositMoneyTransaction, name = 'depositMoney'),
    
]
