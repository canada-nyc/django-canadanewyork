def sentance_join(list):
    '''
    Returns the list joined properly to add to text.

    For example:

    first, second, and third
    first and second
    first
    '''
    if not len(list):
        return ''
    if len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return ' and '.join(list)
    else:
        list[-1] = 'and ' + list[-1]
        return ', '.join(list)


def select_template_name(template_name_list, using=None):
    """
    adapted from https://github.com/django/django/blob/67732a9b183d2e84c85147b04fdf9499f4395ac6/django/template/loader.py#L28-L48

    Loads and returns the first valid template name for one of the given names.
    Tries names in order and returns the first template found.
    Raises TemplateDoesNotExist if no such template exists.
    """
    from django.template.loader import _engine_list
    from django.template.exceptions import TemplateDoesNotExist

    chain = []
    engines = _engine_list(using)
    for template_name in template_name_list:
        for engine in engines:
            try:
                engine.get_template(template_name)
            except TemplateDoesNotExist as e:
                chain.append(e)
            else:
                return template_name
    if template_name_list:
        raise TemplateDoesNotExist(', '.join(template_name_list), chain=chain)
    else:
        raise TemplateDoesNotExist("No template names provided")
