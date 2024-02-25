from django.shortcuts import render, redirect

from django.contrib import messages
# Create your views here.
from .models import Book, Borrow, Review
# from account.models import Account
from transaction.models import Transaction
from .forms import ReviewForm



########### To send Email #############

from django.core.mail import EmailMessage
from django.template.loader import render_to_string # thats will be convert html to string
from django.core.mail import EmailMultiAlternatives


def details(request, id):

    book =  Book.objects.get(id = id)
    # print('book',book)
    bookCategories = book.category.all()
    borrowingRecord = 0
    reviewRecord = -1

    try:
        # print("first")
        borrow = Borrow.objects.filter(account = request.user.account)
        borrow = borrow.filter(book = book)
        # print("second")
        borrowingRecord = len(borrow)
        # print("borrowing record : ", borrowingRecord) # ei khana record check korbo
        # print("last")

        reviewRecord = Review.objects.filter(account = request.user.account)
        reviewRecord = reviewRecord.filter(book = book)
        reviewRecord = len(reviewRecord)

        # print("Review Record :", reviewRecord)

    except:
        borrowingRecord = 0
        reviewRecord = -1


    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login") # an unauthenticated user can't review 
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            # review form theka sob data extract korbo
            review = form.cleaned_data.get("review")
            review_body = form.cleaned_data.get("review_body")
            account = request.user.account
            book = book

            # review er ekta object banabo

            newReview = Review(account = account, book = book, review = review, review_body = review_body)

            messages.success(request, "Review added successfully")

            newReview.save()

            return redirect('details', id)
    else:

        form = ReviewForm()
    # print("book categories :", bookCategories)
    # print("borrowing record :", borrowingRecord, " review record : ", reviewRecord )
    return render(request, 'book_details.html', {"book": book, "form": form, 'borrowingRecord': borrowingRecord, "reviewRecord": reviewRecord, "categories": bookCategories})




def borrowBook(request, id):
    if not  request.user.is_authenticated:
        return redirect("login") 
    else:

        borrowItem = None
        try:
            book  = Book.objects.get(id = id) # first time specific book ka dhorbo

            # print("Catch by its id :", book)

            borrowItem = Borrow.objects.filter(account = request.user.account) # check kora dekhbo ja user already sei book ta borrow korcha ki na. 

            borrowItem = borrowItem.filter(book = book)


            # print("Borrow Item", borrowItem)

            # print("try block kaj korta parcha")


 
            
        except:
            borrowItem = list() # eta dia size track rakhbo
            # print("except block kaj korcha")
         
        if len(borrowItem): # 0 hoila false hoba noyto true hoba
            messages.error(request, "You have already borrowed this book.")
            # print("user already sei book borow korcha")

            return redirect("homepage")
        else:
            book = Book.objects.get(id = id) # book er id dia sei book ka dhorlam

            price = book.borrow_price
            # print('book price is ', price)
            account_balance = request.user.account.balance # user er account er balance ber koralam
            # print("user account balance is :", account_balance)


            if price > account_balance:
                messages.error(request, 'Your Account balance is insufficient.')
                print("user ar balance kom")
                return redirect("homepage")

            else:
                
                # print("ei jaygay kaj korar kotha")
                newBorrowing = Borrow.objects.create(book = book, account = request.user.account )

                newBorrowing.save()

                # ei part a account model nia kaj korta hoba

                account = request.user.account
                account.balance -= price
                account.save() # account ka save korlam

                newTransaction = Transaction(amount = price, balance_after_transaction = account.balance , account = account, borrow = newBorrowing)

                newTransaction.save()



                messages.success(request, "Congratulations! You borrowed this book successfully.")

                mail_subject = "Conformation Borrow Book"
                message = render_to_string('borrowBookMail.html',{"book":book, "price": price, 'balance': account.balance})
                to_email = request.user.email
                send_mail = EmailMultiAlternatives(mail_subject,"", to = [to_email])
                send_mail.attach_alternative(message, 'text/html')
                send_mail.send() # email send kora sesh

                return redirect("profile")



def returnBook(request, id):
    if not request.user.is_authenticated:
        return redirect("login")
    borrow_item = Borrow.objects.get(id = id)
    returnMoney = borrow_item.book.borrow_price
    account = request.user.account
    account.balance += returnMoney
    account.save()
    borrow_item.delete()
    messages.success(request, "Return  book successfully.")
    return redirect("profile")


