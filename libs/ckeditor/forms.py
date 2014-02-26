from django import forms

from .widgets import CKEditorWidget


class CKEditorFormField(forms.fields.Field):

    def __init__(self, *args, **kwargs):
        kwargs.update({'widget': CKEditorWidget()})
        super(CKEditorFormField, self).__init__(*args, **kwargs)
