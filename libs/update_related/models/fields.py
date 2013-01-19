from django.db.models import PROTECT, OneToOneField
# from django.db.models.signals import pre_delete
from django.contrib.sites.models import Site
from django.conf import settings
# from django.dispatch import receiver

from south.modelsinspector import introspector

from libs.redirects.models import Redirect
from .savers import ALL_VALUES


class UpdateOneToOneField(OneToOneField):
    def __init__(self, to, **kwargs):
        kwargs['editable'] = False

        # dictionary of with each field to fill on the related object with a
        # function of taking a model_instance and returning the correct value
        # for that field
        self.model_to_related = kwargs.pop('model_to_related')

        # if the save on function evaluates to true, then the related model
        # will be saved. The function is called with this field,
        # model_instance, and add
        self.save_on = kwargs.pop('save_on', ALL_VALUES)
        super(UpdateOneToOneField, self).__init__(to, **kwargs)

    def _related_kwargs(self, model_instance):
        '''
        Given a instance of the model, will return a dictionary of fields and
        values to save onto the related model.
        '''
        return {field: value_function(model_instance) for field, value_function in self.model_to_related.items()}

    def pre_save(self, model_instance, add):

        OtherModelInstance = getattr(model_instance, self.name)
        if self.save_on(self, model_instance, add):
            if OtherModelInstance:
                OtherModelInstance.__dict__.update(self._related_kwargs(model_instance))
                OtherModelInstance.save()
            else:
                OtherModel = self.related.parent_model
                OtherModelInstance = OtherModel.objects.create(**self._related_kwargs(model_instance))
        else:
            OtherModelInstance = None
        other_model_pk = getattr(OtherModelInstance, 'pk', None)
        setattr(model_instance, self.attname, other_model_pk)
        setattr(model_instance, self.name, OtherModelInstance)
        return other_model_pk

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        args, kwargs = introspector(self)
        field_class = self.__class__.__module__ + "." + self.__class__.__name__
        del kwargs['to']
        return (field_class, args, kwargs)


class RedirectField(UpdateOneToOneField):
    def __init__(self, **kwargs):
        kwargs['model_to_related'] = dict({
            'old_path': lambda model: model.old_path,
            'new_path': lambda model: model.get_absolute_url(),
            'site': lambda model: Site.objects.get(id=settings.SITE_ID)},
            **kwargs.get('model_to_related', {})
        )
        kwargs['on_delete'] = PROTECT
        kwargs['blank'] = kwargs['null'] = True
        super(RedirectField, self).__init__(Redirect, **kwargs)

# @receiver(pre_delete)
# def my_callback(sender, instance, signal, using, **kwargs):
#     for field in sender._meta.fields:
#         if field.__class__ is RedirectField:
#             getattr(instance, field.name).delete()
