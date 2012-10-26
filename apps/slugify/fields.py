from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify

from south.modelsinspector import add_introspection_rules


SLUG_INDEX_SEPARATOR = '-'    # the "-" in "foo-2"


class SlugifyField(SlugField):
    def __init__(self, *args, **kwargs):
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
            values = [slugify(getattr(model_instance, field_name)) for field_name in self.populate_from]
            slug = self.index_sep.join(values)
            setattr(model_instance, self.attname, slug)
            return slug

        return current_value

add_introspection_rules([], [r"^apps\.slugify\.fields\.SlugifyField"])