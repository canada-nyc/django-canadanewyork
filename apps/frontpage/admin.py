from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Frontpage


class FrontpageAdmin(AdminImageMixin, admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('activated', 'date_added', 'exhibition',)
    fieldsets = (
        (None, {
            'fields': ('activated', 'exhibition', 'extra_text'),
        }),
        ('Choose either', {
            'fields': ('exhibition_image', 'uploaded_image',),
        }),
    )

admin.site.register(Frontpage, FrontpageAdmin)
