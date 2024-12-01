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

    def get_queryset(self):
        author_id = self.request.query_params.get('author_id')
        genre_id = self.request.query_params.get('genre_id')
        isbn = self.request.query_params.get('isbn')
        one_copy = self.request.query_params.get('available')


        queryset = Book.objects.all()

        if isbn:
            queryset = queryset.filter(isbn=isbn)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        if genre_id:
            genre_ids_list = genre_id.split(',')
            queryset = queryset.filter(genre_id__in=genre_ids_list)

        if one_copy:
            queryset = queryset.filter(copies_available__gt=0)

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


# register user
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# redirect to corresponding page (staff or student) depending on staff boolean 
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user:

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
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

@api_view(['DELETE'])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def make_reservation(request):
    serializer = ReservationsSerializer(data=request.data)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
    except AssertionError as e:
        error_message = "Error. This book has no copies available to borrow. Would you like to be put in a waitlist instead?"
        return Response({"error": error_message}, status=400)
