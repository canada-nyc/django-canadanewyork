from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.core.exceptions import FieldError

SEP = '-'    # the "-" in "foo-2"
# So that if used in filesystem, will not exceed max file length
MAX_LENGTH = 255 - len('.jpg')


class SlugifyField(SlugField,):

    description = "Auto generated slug (from %(populate_from)s)"

    def __init__(self, populate_from, sep=SEP, max_length=MAX_LENGTH, slug_template=None, *args, **kwargs):
        self.populate_from = populate_from
        self.sep = sep
        self.max_length = kwargs['max_length'] = max_length

        kwargs['editable'] = False

        self.slug_template = slug_template
        if self.slug_template:
            self.slug_joiner = lambda values: self.slug_template.format(*values)
        else:
            self.slug_joiner = lambda values: self.sep.join(values)
        super(SlugifyField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        slug = getattr(model_instance, self.attname)
        if not slug:
            slug = self._get_value(model_instance)
        setattr(model_instance, self.attname, slug)
        return slug

    def _get_value(self, model_instance):
        if isinstance(self.populate_from, str):
            raise FieldError(
                ('In model {}, field {}, the populate_from kwarg needs to '
                 'be passed a list, not a string').format(model_instance,
                                                          self.attname))

        values = [getattr(model_instance, field) for field in self.populate_from]

        slugified_values = list(map(slugify, values))
        slug = self.slug_joiner(slugified_values)
        return slug[:self.max_length]

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)

        original_getattr = cls.__getattribute__

        def __getattribute__(self_, name):
            original = original_getattr(self_, name)
            # if we are trying to get the value of this field,
            # and it has not been set yet, calculate the value and
            # return that
            if name == self.attname and not original:
                return self._get_value(self_)
            return original

        cls.__getattribute__ = __getattribute__

    def deconstruct(self):
        name, path, args, kwargs = super(SlugifyField, self).deconstruct()

        kwargs["populate_from"] = self.populate_from
        if self.sep != SEP:
            kwargs["sep"] = self.sep
        if self.max_length != MAX_LENGTH:
            kwargs["max_length"] = self.max_length
        if self.slug_template is not None:
            kwargs["slug_template"] = self.slug_template

        del kwargs['editable']

        return name, path, args, kwargs
