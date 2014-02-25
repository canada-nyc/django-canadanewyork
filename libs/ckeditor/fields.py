from django.db.models import TextField, SubfieldBase
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from south.modelsinspector import add_introspection_rules

from .forms import CKEditorWidget
from .settings import get_html_class


class CKEditorField(TextField):

    __metaclass__ = SubfieldBase
    description = (
        'A TextField that provides a CKEditor field and an `as_html`` property'
        ' that will wrap the content in a div set to the class of the setting'
        ' ``CKEDITOR_CLASS``')

    def formfield(self, **kwargs):
        defaults = {'widget': CKEditorWidget}
        defaults.update(kwargs)
        return super(CKEditorField, self).formfield(**defaults)

    def to_python(self, value):
        original_value = super(CKEditorField, self).to_python(value)

        class CKEditorString(original_value.__class__):

            @property
            def as_html(self):
                return mark_safe(render_to_string('ckeditor/to_html.html', {
                    'content': original_value,
                    'class': get_html_class(),
                }))
        return CKEditorString(original_value)


add_introspection_rules([], ["^libs\.ckeditor\.fields\.CKEditorField"])
