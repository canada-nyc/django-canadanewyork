from django.contrib import admin

from .models import Update
from libs.common.admin import PhotoInline


class UpdateAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('post_date')
    fields = ('description', 'post_date',)

admin.site.register(Update, UpdateAdmin)
