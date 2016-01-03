from django.db.models import TextField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .settings import get_html_class
from .forms import CKEditorFormField


class CKEditorString(str):

    @property
    def as_html(self):
        return mark_safe(render_to_string('ckeditor/to_html.html', {
            'content': self,
            'class': get_html_class(),
        }))


class CKEditorField(TextField):

    description = (
        'A TextField that provides a CKEditor field and an `as_html`` property'
        ' that will wrap the content in a div set to the class of the setting'
        ' ``CKEDITOR_CLASS``')

    def formfield(self, **kwargs):
        kwargs['form_class'] = CKEditorFormField
        return super(CKEditorField, self).formfield(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        '''
        Change the class so that when this attribute is accessed, it will
        return a `CKEditorString` not a normal string. This is so that
        the `as_html` attribute will be available, even if haven't retrieved
        the field form the DB.
        '''
        super().contribute_to_class(cls, name, **kwargs)

        original_getattr = cls.__getattribute__

        def __getattribute__(self_, name):
            original = original_getattr(self_, name)
            if name == self.attname:
                return CKEditorString(original)
            return original

        cls.__getattribute__ = __getattribute__

    def from_db_value(self, value, expression, connection, context):
        return CKEditorString(value)

    def to_python(self, value):
        if isinstance(value, CKEditorString):
            return value
        return CKEditorString(value)
