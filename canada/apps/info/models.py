from django.db import models
from django.db.models import permalink


class Info(models.Model):
    date_added = models.DateField(auto_now_add=True)
    activated = models.BooleanField(
        verbose_name='Use as frontpage?',
        help_text="To switch frontpages, activate a different one"
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
            Info.objects.all().update(activated=False)
        elif not Info.objects.filter(activated=True).exists():
            self.activated = True
        super(Info, self).save()

    @permalink
    def get_absolute_url(self):
        return ('info-detail', (), {'pk': self.pk})
