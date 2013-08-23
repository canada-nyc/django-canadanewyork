from django import forms
from django.contrib import admin
from django.contrib.contenttypes import generic

from .models import Photo


def photo_inline(photo_class):
    class PhotoForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(PhotoForm, self).__init__(*args, **kwargs)
            self.fields['position'].widget = forms.HiddenInput()

        class Meta:
            model = photo_class

    class PhotoInline(admin.StackedInline):
        model = photo_class
        form = PhotoForm
        sortable_field_name = "position"
        extra = 0

        classes = ('collapse open',)
        inline_classes = ('collapse open',)

    return PhotoInline


class PhotoInline(photo_inline(Photo), generic.GenericStackedInline):
    fields = (
        ('image', "position"),
        'artist_text',
        ('title', 'year'),
        ('height', 'width', 'depth'),
        'medium',
        'caption',
    )
