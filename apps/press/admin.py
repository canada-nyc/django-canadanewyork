from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'publisher', 'link')
        }),
        ('Full Article', {
            'fields': ('content', 'content_file',)
        }),
        ('Related', {
            'fields': ('exhibition', 'artist')
        }),
    )

admin.site.register(Press, PressAdmin)
