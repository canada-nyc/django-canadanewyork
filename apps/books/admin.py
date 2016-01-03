import autocomplete_light
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

    form = autocomplete_light.modelform_factory(Book, fields='__all__')


admin.site.register(Book, BookAdmin)
