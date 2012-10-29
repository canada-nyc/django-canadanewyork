from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.core.exceptions import FieldError

from south.modelsinspector import add_introspection_rules


SLUG_INDEX_SEPARATOR = '-'    # the "-" in "foo-2"


class SlugifyField(SlugField):
    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False

        # autopopulated slug is not editable unless told so
        self.populate_from = kwargs.pop('populate_from')

        # Use default seperator unless given one
        self.index_sep = kwargs.pop('sep', SLUG_INDEX_SEPARATOR)
        super(SlugifyField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # get currently entered slug
        current_value = getattr(model_instance, self.attname)

        # autopopulate
        if not current_value:
            if isinstance(self.populate_from, basestring):
                raise FieldError('In model {}, field {}, the populate_from kwarg needs to be passed a list, not a string'.format(model_instance, self.attname))
            values = [value(model_instance) if callable(value) else getattr(model_instance, value) for value in self.populate_from]
            slug = self.index_sep.join(map(slugify, values))
            setattr(model_instance, self.attname, slug)
            return slug

        return current_value

add_introspection_rules([], [r"^apps\.slugify\.fields\.SlugifyField"])