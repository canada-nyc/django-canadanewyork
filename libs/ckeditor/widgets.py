from django.forms import widgets
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from .settings import get_html_class


class CKEditorWidget(widgets.Textarea):

    class Media:
        js = ('canada/ckeditor/ckeditor.js',)

    def render(self, name, value, attrs=None):
        output = super(CKEditorWidget, self).render(name, value, attrs)
        output += mark_safe(render_to_string('ckeditor/widget.html', {
            'element_id': name,
            'body_class': get_html_class(),
        }))
        return output
