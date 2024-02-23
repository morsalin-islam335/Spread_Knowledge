from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError  # jodi amount kom hoy tahola ei validation error dekhabo.
from .models import Transaction
from account.models import Account
from . forms import TransactionFrom
from django.contrib import messages
# Create your views here.

from django.views.generic import CreateView



########### To send Email #############

from django.core.mail import EmailMessage
from django.template.loader import render_to_string # thats will be convert html to string
from django.core.mail import EmailMultiAlternatives


# class TransactionForBorrowBook(CreateView):
#     template_name = ''
#     form_class = ''

#     def get_success_url(self) -> str:
#         return reverse_lazy('home')
    
#     def form_valid(self, form):
#         amount = form.cleaned_data.get('amount')

#         account_balance = self.request.user.account.balance

#         if amount < account_balance:
#             raise ValidationError("Your account balance is less then amount balance")
        
#         else:

#             account = Account.objects.get(user = self.request.user)

#             account.balance -= amount
#             newTransaction = Transaction(amount = amount, balance_after_transaction = account.balance, account = account)

#             account.save()
#             newTransaction.save()
#         return super().form_valid(form)
    


# def borrowBookTransaction(request):

#     if not request.user.is_authenticated:
#         return redirect("login")
#     else:
#         form = TransactionFrom(request.POST)

#         if request.method == "POST":
#             if form.is_valid():
#                 amount = form.cleaned_data.get('amount')
#                 account = Account.objects.get(user = request.user)
#                 account_balance = account.balance

#                 if amount < account_balance:
#                     raise ValidationError("Your account balance is less then amount balance")
#                 else:
#                     account.balance  -= amount
#                     account.save()

#                     newTransaction = Transaction(amount = amount, balance_after_transaction = account.balance, account = account)
#                     newTransaction.save()

#                     return redirect("home")
#             else:
#                 raise ValidationError("Form information is not correct")
        
#         else:
#             form = TransactionFrom()
#         return render(request, {"form":form})
        


def DepositMoneyTransaction(request):
    if not  request.user.is_authenticated:
        return redirect("login")
    
    else:

        if request.method == "POST":
            form = TransactionFrom(request.POST)

            if form.is_valid():
                amount = form.cleaned_data.get("amount")

                if (amount < 100):
                    messages.error(request, "Minimum Deposit Amount is 100$")
                    return redirect("depositMoney")
                else:
                    account = Account.objects.get(user = request.user)
                    account.balance  += amount
                    account.save()

                    newTransaction = Transaction.objects.create(amount = amount, balance_after_transaction = account.balance, account = account)
                    newTransaction.save()
                    messages.success(request, f"{amount}$  Deposit Successfully!")

                    mail_subject = "Deposit Money"
                    message = render_to_string('depositMail.html',{ "amount": amount, 'balance': account.balance})
                    to_email = request.user.email
                    send_mail = EmailMultiAlternatives(mail_subject,"", to = [to_email])
                    send_mail.attach_alternative(message, 'text/html')
                    send_mail.send() # email send kora sesh

                    return redirect("homepage")
            # else:
            #     raise ValidationError("Form information is incorrect")

        else:

            form = TransactionFrom()
        return render(request,'depositMoney.html', {"form":form})


       
