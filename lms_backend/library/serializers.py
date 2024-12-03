from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import *
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from datetime import timedelta


# validated data is all the parameters sent through the api in json format

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        new_user = LibraryUser.objects.create_user(**validated_data)

        # encrypt password in django
        if password is not None:
            new_user.set_password(password)
            new_user.save()

        return new_user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='author', write_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre', write_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        
    def create(self, validated_data):
        author = validated_data.pop('author')
        genre = validated_data.pop('genre')
        book_copies = validated_data.pop('copies_available', 1)
        
        book = Book.objects.create(author_id=author, genre_id=genre, **validated_data)

        # populate the book copies table automatically upon adding a new book to the inventory
        for copy_num in range(1, book_copies+1):
            Book_Copies.objects.create(book_id=book, book_copy_num=copy_num)

        return book

class BookCopiesSerializer(serializers.ModelSerializer):
    copy_id = serializers.PrimaryKeyRelatedField(queryset=Book_Copies.objects.all(), write_only=True)

    class Meta:
        model = Book_Copies
        fields = '__all__'


class ReservationsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=LibraryUser.objects.all(), write_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Reservations
        fields = '__all__'
        
    def create(self, validated_data):
        desired_book = validated_data.get('book_id')
        user = validated_data.get('user_id')

        # Vesion 2
        # check that the book has at least one copy available 
        # get all copy ids associated with the desired book 
        # iterate through the book's copies and reserve the first available one
        # decrease total amount of copies available for the book by 1
        with transaction.atomic():
            try:
                book = Book.objects.select_for_update().get(book_id=desired_book.book_id)
            except Book.DoesNotExist:
                raise ValidationError("The specified book does not exist.")

            if book.copies_available > 0:
                copy_obj = Book_Copies.objects.select_for_update().filter(
                    book_id=book, is_available=True
                ).first()

                if copy_obj:
                    reservation = Reservations.objects.create(
                        book_id=book, 
                        user_id=user, 
                        copy_id=copy_obj
                    )
                    copy_obj.is_available = False
                    copy_obj.save()
                    book.copies_available -= 1
                    book.save()
                    return reservation
                else:
                    raise ValidationError("No available copies found for reservation.")
            else:
                raise ValidationError("No copies available to reserve. Would you like to join the waitlist?")

        raise ValidationError("An error occurred during reservation. Please try again.")

        # Version 1
        # book = Book.objects.filter(book_id=desired_book.book_id).first()
        # copies_avail = book.copies_available
        #
        # if desired_book:
        #     book = Book.objects.filter(book_id=desired_book.book_id).first()
        #     copies_avail = book.copies_available
        #     if copies_avail > 0:
        #         possible_copies = Book_Copies.objects.filter(book_id=book.book_id)
        #         for copy_obj in possible_copies:
        #             if copy_obj.is_available:
        #                 reservation = Reservations.objects.create(book_id=book, user_id=user, copy_id=copy_obj)
        #                 copy_obj.is_available = False
        #                 copy_obj.save()
        #                 book.copies_available -= 1
        #                 book.save()
        #                 return reservation
        #     else:
        #         error_message = "Error. This book has no copies available to borrow. Would you like to be put in a waitlist instead?"
        #         raise ValidationError(error_message)

class WaitlistSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=LibraryUser.objects.all(), write_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Waitlist
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user_id')
        book = validated_data.get('book_id')

        # Check for existing reservation
        existing_reservation = Reservations.objects.filter(user_id=user, book_id=book).first()
        if existing_reservation:
            raise ValidationError("User already has a reservation for this book.")

        # Check if already on waitlist
        existing_waitlist = Waitlist.objects.filter(user_id=user, book_id=book, book_lent=False).first()
        if existing_waitlist:
            raise ValidationError("User is already in the waitlist for this book.")

        # Create new waitlist entry
        waitlist_entry = Waitlist.objects.create(**validated_data)
        return waitlist_entry
