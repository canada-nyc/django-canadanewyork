from django.db import models
from django.db.models import permalink


class Contact(models.Model):
    date_added = models.DateField(auto_now_add=True)
    activated = models.BooleanField(
        verbose_name='Use as contact/info page??',
        help_text="To switch contact pages, activate a different one"
    )
    text = models.TextField(
        max_length=800,
        help_text=('Show in contact/info page<br>'
                   '<em>To add style:</em> use markdown('
                   '<a href="http://daringfireball.net/projects/markdown/basics"'
                   ' target="_blank">reference</a>)'),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-date_added"]

    def __unicode__(self):
        return str(self.date_added)

    def save(self):
        if self.activated:
            Contact.objects.all().update(activated=False)
        elif not Contact.objects.filter(activated=True).exists():
            self.activated = True
        super(Contact, self).save()

    @permalink
    def get_absolute_url(self):
        return ('contact-detail', (), {'pk': self.pk})
