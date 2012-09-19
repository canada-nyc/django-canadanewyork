from django.db import models
from django.db.models import permalink

from ..fields import UniqueBooleanField


class Info(models.Model):
    date_added = models.DateField(auto_now_add=True)
    activated = UniqueBooleanField(
        verbose_name='Use as contact/info page?',
        help_text="To switch contact/info pages, activate a different one"
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
