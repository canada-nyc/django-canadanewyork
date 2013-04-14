from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('__unicode__', 'publisher', 'date', 'exhibition', 'artist')
    llist_filter = ('publisher', 'date', 'exhibition', 'artist')

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'publisher', 'link')
        }),
        ('Article', {
            'fields': ('content', 'content_file',)
        }),
        ('Related', {
            'fields': ('exhibition', 'artist')
        }),
    )

admin.site.register(Press, PressAdmin)
