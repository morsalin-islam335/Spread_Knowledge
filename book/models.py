from django.db import models
from account.models import Account

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 80, unique = True)
    slug = models.SlugField(max_length = 120)

    def __str__(self):
        return f"Category :{self.name}"


class Book(models.Model):
    image = models.ImageField(upload_to = 'book/media/uploads/')
    title = models.CharField(max_length = 70)
    description = models.TextField()
    category = models.OneToOneField(Category, on_delete = models.CASCADE)

    borrow_price = models.IntegerField(verbose_name = 'borrow price')

    def __str__(self):
        return f"{self.title}"



star = (
    ("⭐","⭐"),
    ("⭐⭐","⭐⭐"),
    ("⭐⭐⭐","⭐⭐⭐"),
    ("⭐⭐⭐⭐","⭐⭐⭐⭐"),
    ("⭐⭐⭐⭐⭐","⭐⭐⭐⭐⭐"),
)

class Review(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE) # an user may have multiple review
    book = models.ForeignKey(Book, on_delete = models.CASCADE) # a book may have multiple review
    review = models.CharField(max_length = 10, choices = star)
    review_body = models.TextField()

    def __str__(self):
        return f" Reviewer : {self.account.user.first_name} book : {self.review_body}"
        


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE)  # a book can borrow multiple user (a book with is not just for an user)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    borrowing_time = models.DateTimeField(auto_now_add = True)


    def  __str__(self):
        return f"borrower {self.account.user.first_name} {self.account.user.last_name} => book : {self.book.title}"