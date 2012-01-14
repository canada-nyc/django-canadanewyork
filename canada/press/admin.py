from django.contrib import admin
from canada.press.models import *


class PressAdmin( admin.ModelAdmin ):
    date_hierarchy = 'date'
    list_display = ('date', 'title', 'publisher', 'exhibition', 'slug')

admin.site.register( Press, PressAdmin )
