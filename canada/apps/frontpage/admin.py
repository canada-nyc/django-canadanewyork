from django.contrib import admin

from .models import Frontpage
from ..admin import image_file


class FrontpageAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('image_thumb', 'activated', 'date_added', 'exhibition',)

    fieldsets = (
        ('', {
            'fields': ('activated', 'custom_title', 'uploaded_image', 'text',),
        }),
        ('Link to Exibition', {
            'classes': ('grp-collapse',),
            'fields': ('exhibition', 'exhibition_image', 'exhibition_text'),
        }),
        ('Link to Update', {
            'classes': ('grp-collapse',),
            'fields': ('update', 'update_image', 'update_text'),
        }),
    )

    image_thumb = image_file('obj.image()')


admin.site.register(Frontpage, FrontpageAdmin)
