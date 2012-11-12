from django.contrib import admin
from django import forms

from .models import Update, UpdatePhoto


class UpdatePhotoInlineForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class UpdatePhotoInline(admin.TabularInline):
    model = UpdatePhoto
    form = UpdatePhotoInlineForm
    sortable_field_name = "position"


class UpdateAdmin(admin.ModelAdmin):
    inlines = [UpdatePhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('name', 'post_date')
    fields = ('name', 'description', 'old_path')

admin.site.register(Update, UpdateAdmin)
