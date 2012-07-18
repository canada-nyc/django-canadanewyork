import os

from django.db import models


class ContactList(models.Model):
    name = models.CharField(max_length=50, unique=True)
    default = models.BooleanField(
        verbose_name='Default List',
        help_text=('Emails submitted via the forum on the website will use the'
                   'default list')
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self):
        if self.default:
            ContactList.objects.all().update(default=False)
        if not ContactList.objects.filter(default=True).exists():
            self.default = True
        super(ContactList, self).save()


class Message(models.Model):
    def image_path(instance, filename):
        return os.path.join('bulkmail',
                            str(instance.pk),
                            filename)

    date_time = models.DateTimeField(auto_now_add=True, editable=False)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to=image_path)
    contact_list = models.ForeignKey(ContactList)

    class Meta:
        ordering = ['-date_time']

    def __unicode__(self):
        return u'{} at {} ({})'.format(self.subject, self.date_time, self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('message-detail', (), {
            'pk': self.pk,
            })


class Contact(models.Model):
    email = models.EmailField(unique=True)
    contact_list = models.ForeignKey(ContactList, related_name='contacts')

    class Meta:
        ordering = ['contact_list', 'email']

    def __unicode__(self):
        return u'{} in {}'.format(self.email, self.list)
