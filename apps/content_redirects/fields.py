from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db.models import CharField
from django.db import IntegrityError

from south.modelsinspector import add_introspection_rules


class RedirectOldPathField(CharField):
    def __init__(self, redirect_field, *args, **kwargs):
        if 'django.contrib.redirects' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured('Include `django.contrib.redirects` in'
                                       ' INSTALLED_APPS, for `content_redirects`')
        self.redirect_field = redirect_field
        self.site_id = kwargs.get('site_id', settings.SITE_ID)
        kwargs['max_length'] = 200
        super(RedirectOldPathField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        old_path = getattr(model_instance, self.attname)
        new_path = model_instance.get_absolute_url()
        redirect = getattr(model_instance, self.redirect_field)
        site = Site.objects.get(id=self.site_id)

        try:
            if old_path:
                if redirect:
                    redirect.old_path = old_path
                    redirect.new_path = new_path
                    redirect.site = site
                else:
                    redirect = Redirect.objects.create(old_path=old_path, new_path=new_path,
                                                       site=site)
                    setattr(model_instance, self.redirect_field, redirect)
            else:
                if redirect:
                    redirect.delete()
        except IntegrityError as error:
            raise ValidationError('{} conflicts with another redirect, within site {}, Error: {}'.format(self.attname, site, str(error)))
        return old_path

add_introspection_rules([], [r"^apps\.content_redirects\.fields\.RedirectOldPathField"])
