from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
# Register your models here.

class LibraryUserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),  # 'date_joined' is omitted here
    )

    list_display = ['first_name', 'last_name', 'email', 'is_staff']
    ordering = ['email']  # Set the default ordering field
    
    list_filter = ['is_staff'] 

admin.site.register(LibraryUser, LibraryUserAdmin)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_id', 'release_date', 'isbn']

    # def display_release_date(self, obj):
    #     return obj.release_date.strftime('%d %b %Y')  # Format date as dd mm yyyy
    # display_release_date.short_description = 'Release Date'

@admin.register(Book_Copies)
class Book_copiesAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'book_copy_num', 'is_available']

@admin.register(Reservations)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'user_id', 'start_date', 'due_date']

@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'user_id', 'date_placed']

