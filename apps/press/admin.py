from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'title', 'publisher', 'exhibition',)

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'publisher', 'author', 'link')
        }),
        ('Full Article', {
            'fields': ('content', 'content_file',)
        }),
        ('Related', {
            'fields': ('exhibition', 'artists')
        }),
    )

admin.site.register(Press, PressAdmin)
