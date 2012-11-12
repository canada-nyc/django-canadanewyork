from django.contrib import admin
from django import forms

from sorl.thumbnail.admin import AdminImageMixin

from .models import Exhibition, ExhibitionPhoto


class ExhibitionPhotoInlineForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class ExhibitionPhotoInline(AdminImageMixin, admin.TabularInline):
    model = ExhibitionPhoto
    form = ExhibitionPhotoInlineForm
    sortable_field_name = "position"


class ExhibitionAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [ExhibitionPhotoInline]
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date')
    fields = ('name', 'description', ('start_date', 'end_date'), 'artists', 'old_path')

admin.site.register(Exhibition, ExhibitionAdmin)
