from django.contrib import admin

from .models import Press, Publisher


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'title', 'publisher', 'exhibition', 'slug')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'homepage')

admin.site.register(Press, PressAdmin)
admin.site.register(Publisher, PublisherAdmin)
