from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Frontpage
from ..common.admin import image_file


class FrontpageAdmin(AdminImageMixin, admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('image_thumb', 'activated', 'date_added', 'exhibition',)

    image_thumb = image_file('obj.image()')


admin.site.register(Frontpage, FrontpageAdmin)
