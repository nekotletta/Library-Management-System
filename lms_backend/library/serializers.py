from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import *
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='author', write_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre', write_only=True)


    def create(self, validated_data):
        author = validated_data.pop('author')
        genre = validated_data.pop('genre')
        book_copies = validated_data.pop('copies_available', 1)
        
        book = Book.objects.create(author_id=author, genre_id=genre, **validated_data)

        # populate the book copies table automatically upon adding a new book to the inventory
        for copy_num in range(1, book_copies+1):
            Book_Copies.objects.create(book_id=book, book_copy_num=copy_num)

        return book


    class Meta:
        model = Book
        fields = '__all__'

class BookCopiesSerializer(serializers.ModelSerializer):
    book_id = BookSerializer()

    class Meta:
        model = Book_Copies
        fields = '__all__'

class ReservationsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=LibraryUser.objects.all(), source='user_id', write_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book_id', write_only=True)
    # copy_id = serializers.PrimaryKeyRelatedField(queryset=Book_Copies.objects.all(), source='book_copies', write_only=True)

    def create(self, validated_data):
        print(validated_data)
        # Extracting book_id if present
        book_id = validated_data.get('book_id')
        user_id = validated_data.get('user_id')


        # Filtering copy_id queryset based on the selected book_id
        if book_id:
            book = Book.objects.filter(book_id=book_id).first()
            copies_avail = book.copies_available


            # if copies_avial <= 0:
            #     raise ValidationError("The book you wish to reserve has no copies available at the moment.")
            if copies_avail > 0:
                possible_copies = Book_Copies.objects.filter(book_id=book_id)
                for copy_obj in possible_copies:
                    if copy_obj.is_available:
                        reservation = Reservations.objects.create(book_id=book_id, user_id=user_id, copy_id=copy_obj.copy_id)
                        copy_obj.is_available = False
                        copy_obj.save()
                        return reservation
            else:
                error_message = "Error. This book has no copies available to borrow. Would you like to be put in a waitlist instead?"
                raise ValidationError(error_message)
            

        

    class Meta:
        model = Reservations
        fields = '__all__'

class WaitlistSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=LibraryUser.objects.all(), source='libraryuser', write_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)

    class Meta:
        model = Waitlist
        fields = '__all__'