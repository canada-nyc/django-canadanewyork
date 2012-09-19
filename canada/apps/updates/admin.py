from django.contrib import admin
from django import forms

from .models import Update, UpdatePhoto
from .._base.admin import image_file


class UpdatePhotoInlineForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class UpdatePhotoInline(admin.TabularInline):
    model = UpdatePhoto
    form = UpdatePhotoInlineForm
    sortable_field_name = "position"


class UpdateAdmin(admin.ModelAdmin):
    inlines = [UpdatePhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('first_image_thumb', 'name', 'post_date')

    first_image_thumb = image_file('obj.get_first_image_or_none().image',
                                   'First Image')
admin.site.register(Update, UpdateAdmin)
