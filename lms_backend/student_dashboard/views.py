from django.shortcuts import render
from librarian_dashboard.models import *
from user_reg.models import *

# Create your views here.
def student_main_page(request):
    all_books = Book.objects.all()
    all_book_obj = []
    for book in all_books:
        print(book.title)
        print(book.author_id)
        print(book.release_date)
        print(book.genre_id)
        print(book.isbn)
    return render(request, 'dashboard.html')