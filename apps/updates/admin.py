from django.contrib import admin

from .models import Update
from ..common.admin import PhotoInline


class UpdateAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('name', 'post_date')
    fields = ('name', 'description',)

admin.site.register(Update, UpdateAdmin)
