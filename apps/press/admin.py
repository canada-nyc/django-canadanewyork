from django.contrib import admin

from .models import Press


class PressAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'title', 'publisher', 'exhibition', 'slug')

    fields = (('title', 'date'), ('publisher', 'author'), 'content', ('image', 'link'), ('exhibition', 'artists',), 'old_path')

    def queryset(self, request):
        return Press.all_objects

admin.site.register(Press, PressAdmin)
