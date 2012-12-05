from django.db.models import SET_NULL
from django.db.models.fields.related import OneToOneField
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from south.modelsinspector import introspector


DEFAULT_GETTERS = {
    'old_path': 'old_path',
    'new_path': lambda model: model.get_absolute_url(),
    'site': lambda model: Site.objects.get(id=settings.SITE_ID),
}


class RedirectField(OneToOneField):
    def __init__(self, **kwargs):
        kwargs['editable'] = False
        kwargs['blank'] = kwargs['null'] = True
        kwargs['on_delete'] = SET_NULL

        self.redirect_getters = {}
        for field, value in DEFAULT_GETTERS.items():
            getter = kwargs.pop(field, value)
            if not callable(getter):
                field_name = getter
                getter = lambda model: getattr(model, field_name)
            self.redirect_getters[field] = getter

        super(RedirectField, self).__init__(Redirect, **kwargs)

    def pre_save(self, model_instance, add):
        redirect_kwargs = {}
        for field, getter in self.redirect_getters.items():
            redirect_kwargs[field] = getter(model_instance)

        redirect = getattr(model_instance, self.name)
        if all(redirect_kwargs.values()):
            if redirect:
                redirect.__dict__.update(redirect_kwargs)
                redirect.save()
            else:
                redirect = Redirect.objects.create(**redirect_kwargs)
        else:
            if redirect:
                redirect.delete()
        id = getattr(redirect, 'id', None)
        setattr(model_instance, self.attname, id)
        setattr(model_instance, self.name, redirect)
        return id

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        args, kwargs = introspector(self)
        field_class = self.__class__.__module__ + "." + self.__class__.__name__
        kwargs.update(
            {field: 'None' for field in DEFAULT_GETTERS.keys()}
        )
        return (field_class, args, kwargs)


@receiver(pre_delete)
def my_callback(sender, instance, signal, using, **kwargs):
    for field in sender._meta.fields:
        if field.__class__ is RedirectField:
            getattr(instance, field.name).delete()
