from django.contrib import admin
import autocomplete_light


from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('title', 'publisher', 'author', 'date', 'exhibition', 'artist')
    list_filter = ('publisher', 'date', 'exhibition', 'artist')
    readonly_fields = ('slug',)

    fieldsets = (
        (None, {
            'fields': (
                'slug',
                'title',
                ('date', 'date_text'),
                'publisher',
                'author',
                'pages_range',
            ),
        }),
        ('Article', {
            'classes': ('full-width',),
            'fields': ('content', 'content_file', 'content_link')
        }),
        ('Related to', {
            'fields': ('exhibition', 'artist')
        }),
    )

    form = autocomplete_light.modelform_factory(Press, fields='__all__')


admin.site.register(Press, PressAdmin)
