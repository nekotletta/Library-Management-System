from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils import timezone
import os
import re
import datetime


from django.contrib.auth.models import BaseUserManager

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set and hash the password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        self.create_user(email, password, **extra_fields) # Creo q esto puede ser el return?

        # return user

class LibraryUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, verbose_name="Apellidos")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Correo electrónico")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    is_staff = models.BooleanField(default=False, verbose_name="Admin")

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["name"]

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    name = models.CharField(max_length=100)  # Author name

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    name = models.CharField(max_length=50)  # Genre name (e.g., Fiction, Non-Fiction)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    title = models.CharField(max_length=100)  # Book title
    release_date = models.DateField(default=datetime.date(1001,1,1))
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)  # Author ID
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, default=1)  # Genre ID
    isbn = models.CharField(max_length=13, unique=True)  # ISBN number
    copies_available = models.IntegerField(default=1)  # Number of copies available
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Book_Copies(models.Model):
    copy_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)  # Book ID
    book_copy_num = models.IntegerField()
    is_available = models.BooleanField(default=True)  # Availability status

    def __str__(self):
        return str(self.copy_id)

class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    user_id = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, default=1)  # User ID
    copy_id = models.ForeignKey(Book_Copies, on_delete=models.CASCADE, default=1)  # Copy ID
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)  # Book ID
    start_date = models.DateField(auto_now_add=True)  # Reservation date
    due_date = models.DateField(default=datetime.date.today() + timezone.timedelta(days=30))

    def __str__(self):
        return str(self.reservation_id)


class Waitlist(models.Model):
    queue_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    user_id = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, default=1)  # User ID
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)  # Book ID
    date_placed = models.DateField(auto_now_add=True)  # Date added to waitlist
    limit_date = models.DateField(blank=True, null=True)  # Date limit for reservation
    book_lent = models.BooleanField(default=False)  # Book lent status
    next_in_line = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.next_in_line:  # Check if the record is being created
            self.limit_date = self.date_placed + timezone.timedelta(days=3)
        super(Waitlist, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.queue_id)
