from django.contrib import admin

from apps.photos.admin import PhotoInline
from .models import Update, UpdatePhoto


class UpdatePhotoInline(PhotoInline):
    model = UpdatePhoto


class UpdateAdmin(admin.ModelAdmin):
    inlines = [UpdatePhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('post_date',)
    fieldsets = [
        (None, {
            'fields': ('post_date', 'description',),
            'classes': ('full-width',),

        }),
    ]

admin.site.register(Update, UpdateAdmin)
