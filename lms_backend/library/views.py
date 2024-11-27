from django.shortcuts import render
from rest_framework import viewsets
from .models import * 
from .serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view


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
        one_copy = self.request.query_params.get('available')


        queryset = Book.objects.all()

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

