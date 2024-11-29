from rest_framework import serializers
from .models import *

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
    author_id = AuthorSerializer()
    genre_id = GenreSerializer()

    class Meta:
        model = Book
        fields = '__all__'

class BookCopiesSerializer(serializers.ModelSerializer):
    book_id = BookSerializer()

    class Meta:
        model = Book_Copies
        fields = '__all__'

class ReservationsSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    book_id = BookSerializer()
    copy_id = BookCopiesSerializer()

    class Meta:
        model = Reservations
        fields = '__all__'

class WaitlistSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    book_id = BookSerializer()

    class Meta:
        model = Waitlist
        fields = '__all__'