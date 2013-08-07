from django import forms
from django.contrib.contenttypes import generic

from .models import Photo

class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget = forms.HiddenInput()

    class Meta:
        model = Photo

class PhotoInline(generic.GenericStackedInline):
    model = Photo
    form = PhotoForm
    sortable_field_name = "position"
    extra = 0

    classes = ('collapse open',)
    inline_classes = ('collapse open',)
    fieldsets = (
        ('', {
            'fields': (('image', "position"),),
        }),
        ('Info (click to expand)', {
            'description': 'Caption will be displayed with any filled in fields:</br>' + Photo.create_mock().full_caption,
            'classes': ('grp-collapse grp-closed',),
            'fields' : ('title', ('height', 'width', 'depth'), 'year', 'medium', 'caption',),
        }),
    )
