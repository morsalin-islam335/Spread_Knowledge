from django.shortcuts import render 

from book.models import Category, Book


def home(request, catSlug = None):
  categories = Category.objects.all()
  totalResult = None
  books = Book.objects.all()
  if catSlug is not None:
    categories = Category.objects.get(slug = catSlug)
    books = Book.objects.filter(category = categories)
    categories = Category.objects.all() # abar o  sob gulo nilam jata search korar somoy filter kora jay
    totalResult = len(books)
  
  return render(request,'home.html', {"categories":categories, "books": books, 'total': totalResult})


 
