from django.contrib import admin

from apps.photos.admin import PhotoInline
from libs.common.admin import editor_form
from .models import Update


class UpdateAdmin(admin.ModelAdmin):
    form = editor_form(['description'])
    inlines = [PhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('post_date',)
    readonly_fields = ('post_date',)
    fieldsets = [
        (None, {
            'fields': ('post_date', 'description',),
            'classes': ('full-width',),

        }),
    ]

admin.site.register(Update, UpdateAdmin)
