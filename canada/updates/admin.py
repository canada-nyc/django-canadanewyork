from django.contrib import admin
from django import forms
from canada.updates.models import Update, UpdatePhoto


class UpdatePhotoForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class UpdatePhotoInline(admin.TabularInline):
    model = UpdatePhoto
    form = UpdatePhotoForm
    sortable_field_name = "position"


class UpdateAdmin(admin.ModelAdmin):
    inlines = [UpdatePhotoInline]
    date_hierarchy = 'post_date'
    list_display = ('name', 'post_date')

admin.site.register(Update, UpdateAdmin)
