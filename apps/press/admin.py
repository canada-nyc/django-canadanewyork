from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'title', 'publisher', 'exhibition', 'slug')

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'publisher', 'author', 'link')
        }),
        ('Full Article', {
            'fields': ('content', 'add_image', 'pdf')
        }),
        ('Related', {
            'fields': ('exhibition', 'artists')
        }),
    )

    def queryset(self, request):
        return Press.all_objects

admin.site.register(Press, PressAdmin)
