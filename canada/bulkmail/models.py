import os

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError


class ContactList(models.Model):
    name = models.CharField(max_length=50)
    default = models.BooleanField(
        verbose_name='Default List',
        help_text="""Whether this contact list is the one that emails are added
        to from the website.
        When someone submits their email on the site, it will be added to the
        contact list that has this checked.
        <br> To enable a different contact list as the default, simply check
        that one. All others will be disabled."""
       )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self):
        if self.default:
            ContactList.objects.all().update(default=False)
        super(ContactList, self).save()

    def clean(self):
        if not self.default:
            try:
                ContactList.objects.exclude(pk=self.pk).get(default=True)
            except ContactList.DoesNotExist:
                raise ValidationError("Enable a different contact list to \
                                       change the default.")


class Message(models.Model):
    def image_path(instance, filename):
        return os.path.join('bulkmail',
                            [instance.date_time, instance.subject].join('-'),
                            filename)

    date_time = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to=image_path)
    list = models.ForeignKey(ContactList)

    class Meta:
        ordering = ['-date_time']

    def __unicode__(self):
        return u'%s at %s' % (self.subject, self.date_time)

    @models.permalink
    def get_absolute_url(self):
        return ('message_html', (), {
            'pk': self.pk,
            })


class Contact(models.Model):
    email = models.EmailField(unique=True)
    list = models.ForeignKey(ContactList)

    class Meta:
        ordering = ['list', 'email']

    def __unicode__(self):
        return u'%s in %s' % (self.email, self.list)


class ContactEmailForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('list')
