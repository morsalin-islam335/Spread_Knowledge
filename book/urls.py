from django.urls import path



from .views import  details, borrowBook, returnBook
urlpatterns = [
    path("details/<int:id>/", details, name = 'details'),
    path("borrowBook/<int:id>", borrowBook, name = 'borrowBook'),
    path("returnBook/<int:id>", returnBook, name = 'returnBook'),
]
