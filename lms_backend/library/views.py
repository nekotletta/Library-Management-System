from django.shortcuts import render
from rest_framework import viewsets
from .models import * 
from .serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models.functions import ExtractYear


class UserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = UserSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer 

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # multiple filtering options for book records
    # to filter results: hosting_url/?param="options"
    def get_queryset(self):
        author_id = self.request.query_params.get('author_id')
        genre_id = self.request.query_params.get('genre_id')
        isbn = self.request.query_params.get('isbn')
        avail = self.request.query_params.get('available')

        # filter by either a single publication year of a range of years
        # for a single year start and end year are the same
        start_year = self.request.query_params.get('start_year')
        end_year = self.request.query_params.get('end_year')


        queryset = Book.objects.all()

        if isbn:
            queryset = queryset.filter(isbn=isbn)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        # can look for books of more than one genre
        if genre_id:
            genre_ids_list = genre_id.split(',')
            queryset = queryset.filter(genre_id__in=genre_ids_list)

        if avail:
            queryset = queryset.filter(copies_available__gt=0)
        
        if start_year and end_year:
            year_range = range(int(start_year), int(end_year) + 1)  # Generate a range of years between start and end years
            queryset = queryset.annotate(release_year=ExtractYear('release_date')).filter(release_year__in=year_range)

        return queryset

class BookCopiesViewSet(viewsets.ModelViewSet):
    queryset = Book_Copies.objects.all()
    serializer_class = BookCopiesSerializer

    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        available = self.request.query_params.get('available')

        queryset = Book_Copies.objects.all()

        if book_id:
            queryset = queryset.filter(book_id=book_id)
        
        if available:
            queryset = queryset.filter(is_available=True)

        return queryset

class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer

class WaitlistViewSet(viewsets.ModelViewSet):
    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_user_info(request, user_id):
    try:
        user = LibraryUser.objects.get(user_id=user_id)
    except LibraryUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password) 
    # redirect to corresponding page (staff or student) depending on staff boolean 
    user_inst = LibraryUser.objects.filter(email=email).first()

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'staff' : user_inst.is_staff})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def add_author(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def add_genre(request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_book(request):
    book_id = request.data.get('book_id')
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def make_reservation(request):
    serializer = ReservationsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def extend_reservation(request):
    reservation_id = request.data.get('reservation_id')
    try:
        reservation_instance = Reservations.objects.get(reservation_id=reservation_id)
    except Reservations.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check that another student is not waiting to borrow the same book
    desired_book = reservation_instance.book_id.book_id
    try:
        book = Waitlist.objects.get(book_id=desired_book)
        return Response(data={"message": "Book is in the waitlist. Unable to extend reservation. Would you like to be placed in the waitlist?"}, status=status.HTTP_400_BAD_REQUEST)
    except Waitlist.DoesNotExist:
        new_due_date = reservation_instance.due_date + timezone.timedelta(days=30)
        reservation_instance.due_date = new_due_date
        reservation_instance.save()
        return Response(data={"message": "Book due date extended successfully"}, status=status.HTTP_200_OK)

    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def return_book(request):
    reservation_id = request.data.get('reservation_id')
    try:
        reservation_instance = Reservations.objects.get(reservation_id=reservation_id)
    except Reservations.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # a user reserves a specific copy. since it's being returned. this copy becomes available again
    reserved_copy = Book_Copies.objects.filter(copy_id=reservation_instance.copy_id.copy_id).first()
    reserved_copy.is_available = True
    reserved_copy.save()

    # at least one book copy is available again
    book = Book.objects.filter(book_id=reservation_instance.book_id.book_id).first()
    book.copies_available += 1
    book.save()

    reservation_instance.delete()
    return Response(data={"message": "Book returned successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_to_waitlist(request):
    serializer = WaitlistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
