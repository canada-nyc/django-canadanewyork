# These are functions for the save_on kwarg for UpdateForeignKey

# save_on and delete_on will be called with the field, the model instance, and whether the
# model is being added for the first time. The truthiness of its ouput will
# determine whether the related model is saved or not.


def ALWAYS(field, model_instance, add):
    return True


def ALL_VALUES(field, model_instance, add):
    return all(field._related_kwargs(model_instance).values())


def ADD(field, model_instance, add):
    return add
