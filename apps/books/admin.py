from django.contrib import admin

import autocomplete_light

from apps.photos.admin import PhotoInline
from .models import Book, BookPhoto


class BookPhotoInline(PhotoInline):
    model = BookPhoto


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'date_text', 'price')
    list_filter = ('artist',)
    date_hierarchy = 'date'

    fields = (
        'title',
        'artist',
        ('price', 'out_of_stock'),
        ('date', 'date_text'),
        'description',
    )

    form = autocomplete_light.modelform_factory(Book, fields='__all__')

    inlines = [BookPhotoInline]


admin.site.register(Book, BookAdmin)
