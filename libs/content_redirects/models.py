from django.db import models
from django.contrib.redirects.models import Redirect
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class BaseRedirectModel(models.Model):
    redirect = models.OneToOneField(Redirect, blank=True, null=True, editable=False)
    old_path = models.CharField(blank=True, null=True, max_length=200, editable=False,
                                help_text='If provided, will redirect from this URL to the new URL. For instance "/exhibitions/old-one" would take any visitor from that URL to the URL of this object')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseRedirectModel, self).save(*args, **kwargs)
        if 'django.contrib.redirects' not in settings.INSTALLED_APPS:
            raise ValidationError('Include `django.contrib.redirects` in'
                                  ' INSTALLED_APPS, for `content_redirects`')

        # Need to get QuerySet so that I can use the update method on it
        # The update method does not call save again, so I can just save the
        # fields without recalling this method.
        self_quersyet = self.__class__.objects.filter(id=self.id)

        if self.old_path:
            redirect_kwargs = {
                'site': Site.objects.get(id=settings.SITE_ID),
                'new_path': self.get_absolute_url(),
                'old_path': self.old_path,
            }
            try:
                if self.redirect:
                    for k, v in redirect_kwargs.items():

                        setattr(self.redirect, k, v)
                        self.redirect.save()
                else:
                    redirect = Redirect.objects.create(**redirect_kwargs)
                    self_quersyet.update(redirect=redirect)
            except IntegrityError as error:
                raise ValidationError(
                    'old_path: {} conflicts with another redirect, within site {}, Error: {}'.format(
                        redirect_kwargs['old_path'],
                        redirect_kwargs['site'],
                        str(error)
                    )
                )
        else:
            if self.redirect:
                self.redirect.delete()
                self_quersyet.update(redirect=None)

    def delete(self, *args, **kwargs):
        if self.redirect:
            self.redirect.delete()
            self.redirect = None
        super(BaseRedirectModel, self).delete(*args, **kwargs)
