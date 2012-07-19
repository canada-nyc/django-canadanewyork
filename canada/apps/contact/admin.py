from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('activated', 'date_added',)

admin.site.register(Contact, ContactAdmin)
