from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Frontpage


class FrontpageAdmin(AdminImageMixin, admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('activated', 'date_added', 'exhibition',)


admin.site.register(Frontpage, FrontpageAdmin)
