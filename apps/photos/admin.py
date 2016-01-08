from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin


class PhotoInline(SortableInlineAdminMixin, admin.StackedInline):
    extra = 0

    classes = ('collapse',)

    fields = (
        "position",
        'image',
        ('title', 'caption'),
    )
