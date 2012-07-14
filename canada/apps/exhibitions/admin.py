from django.contrib import admin
from django import forms

from .models import Exhibition, ExhibitionPhoto
from ..admin import image_file


class ExhibitionPhotoInlineForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class ExhibitionPhotoInline(admin.TabularInline):
    model = ExhibitionPhoto
    form = ExhibitionPhotoInlineForm
    sortable_field_name = "position"


class ExhibitionAdmin(admin.ModelAdmin):
    inlines = [ExhibitionPhotoInline]
    date_hierarchy = 'start_date'
    list_display = ('first_image_thumb', 'name', 'start_date')

    first_image_thumb = image_file('obj.get_first_image_or_none().image',
                                   'First Image')

admin.site.register(Exhibition, ExhibitionAdmin)
