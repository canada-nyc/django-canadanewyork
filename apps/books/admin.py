from django.contrib import admin

from .models import Book


class BookInline(admin.TabularInline):
    model = Book
