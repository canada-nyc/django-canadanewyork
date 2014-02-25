from django.contrib import admin

from .models import CustomPage


class CustomPageAdmin(admin.ModelAdmin):
    model = CustomPage
    list_display = ('path', )

admin.site.register(CustomPage, CustomPageAdmin)
