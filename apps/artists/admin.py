from django.contrib import admin
from django import forms

from .models import Artist, ArtistPhoto


class ArtistPhotoForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class ArtistPhotoInline(admin.TabularInline):
    model = ArtistPhoto
    form = ArtistPhotoForm
    sortable_field_name = "position"
    verbose_name_plural = 'Images'


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistPhotoInline]
    fields = (('first_name', 'last_name'), 'old_path',)
    list_display = ('first_name', 'last_name', 'visible')


admin.site.register(Artist, ArtistAdmin)
