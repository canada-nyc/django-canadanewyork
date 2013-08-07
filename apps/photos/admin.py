from django import forms
from django.contrib.contenttypes import generic

from .models import Photo


class PhotoForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class PhotoInline(generic.GenericTabularInline):
    model = Photo
    form = PhotoForm
    sortable_field_name = "position"
    extra = 0
