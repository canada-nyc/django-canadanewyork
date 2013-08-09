import new

from django.db.models import BooleanField

from south.modelsinspector import add_introspection_rules


class UniqueBooleanField(BooleanField):
    def pre_save(self, model_instance, add):
        attribute_name = self.attname
        value = getattr(model_instance, attribute_name)
        if value:
            self._other_model_objects(model_instance).update(**{attribute_name: False})
        return value

    def _other_model_objects(self, model_instance):
        objects = model_instance.__class__.objects
        return objects.exclude(id=model_instance.id)


add_introspection_rules([], ["^libs\.unique_boolean\.fields\.UniqueBooleanField"])
