import new

from django.db.models import BooleanField

from south.modelsinspector import add_introspection_rules


class UniqueBooleanField(BooleanField):
    def pre_save(self, model_instance, add):
        if self._get_value(model_instance):
            self._other_model_objects(model_instance).update(**{self.attname: False})

        return self._get_value(model_instance)

    def _get_value(self, model_instance):
        # If value is true, then always save as true
        if getattr(model_instance, self.attname):
            return True

        # Else if no other models have true selected, then also return true
        other_true_models = self._other_model_objects(model_instance).filter(
            **{self.attname: True}
        )
        if not other_true_models.exists():
            return True
        return False

    def _other_model_objects(self, model_instance):
        objects = model_instance.__class__.objects
        return objects.exclude(id=model_instance.id)

    def contribute_to_class(self, cls, name):
        super(UniqueBooleanField, self).contribute_to_class(cls, name)
        setattr(
            cls,
            '_get_{}_value'.format(self.name),
            new.instancemethod(
                self._get_value,
                None,
                cls
            )
        )

add_introspection_rules([], ["^libs\.unique_boolean\.fields\.UniqueBooleanField"])
