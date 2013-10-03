from django.contrib import admin

from .models import Book


class BookInline(admin.TabularInline):
    model = Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'date_text')
    list_filter = ('artist',)
    date_hierarchy = 'date'

    fields = (
        'title',
        ('date', 'date_text'),
        'artist'
    )

    raw_id_fields = ('artist',)
    autocomplete_lookup_fields = {
        'fk': ['artist'],
        'm2m': ['related_m2m'],
    }

admin.site.register(Book, BookAdmin)
