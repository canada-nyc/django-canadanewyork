from django.contrib import admin

from .models import Info


class InfoAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('activated', 'date_added',)

admin.site.register(Info, InfoAdmin)
