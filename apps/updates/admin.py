from django.contrib import admin

from .models import Update
from apps.photos.admin import PhotoInline


class UpdateAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('post_date',)
    fields = ('description',)

admin.site.register(Update, UpdateAdmin)
