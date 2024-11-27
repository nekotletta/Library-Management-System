# from rest_framework import serializers
# from .models import *

# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = '__all__'

# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = '__all__'

# class BookSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer()
#     genre = GenreSerializer()

#     class Meta:
#         model = Book
#         fields = '__all__'

# class BookCopiesSerializer(serializers.ModelSerializer):
#     book_id = BookSerializer()

#     class Meta:
#         model = Book_Copies
#         fields = '__all__'
