import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError


from canada.artists.models import Artist
from canada.functions import cap


class Exhibition(models.Model):
    def image_path(instance, filename):
        return os.path.join(
            'exhibitions',
            str(instance.start_date.year),
            str(instance.slug),
            'frontpage-{}'.format(filename)
           )

    name = models.CharField(max_length=30, unique_for_year='start_date')
    description = models.TextField(blank=True)

    frontpage = models.BooleanField(
        verbose_name='Displayed on frontpage?',
        help_text="Checking will use this exhibition for the front page. To change to a different exhibition, simply enable this on that exhibition"
       )
    frontpage_uploaded_image = models.ImageField(
        upload_to=image_path,
        verbose_name='Upload frontpage image',
        blank=True,
        null=True
       )
    frontpage_selected_image = models.ForeignKey(
        'ExhibitionPhoto',
        related_name='frontpage_selected_image',
        verbose_name='Select frontpage image',
        help_text='Uploaded image will take preference. Clear the uploaded image to use the selected image.',
        blank=True,
        null=True,
       )
    frontpage_text = models.TextField(
        max_length=800,
        verbose_name='Text to be added to home page',
        help_text="""Will be added underneath exhibition info<br>
                    <i>To add style refer to the
                    <a href="http://en.wikipedia.org/wiki/Markdown#Syntax_examples"  target="_blank">Wikipedia entry on Markdown</a>
                    or the <a href="http://daringfireball.net/projects/markdown/basics"  target="_blank">Markdown reference</a></i>""",
        blank=True,
        null=True,
       )

    artists = models.ManyToManyField(Artist)
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(blank=True, editable=False)

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        return '%s-%s' % (self.start_date.strftime("%Y"), self.name)

    def save(self):
        cap(self, 'name')
        self.slug = slugify(self.name)

        # sets "frontpage" to False on all other exhibitions, if we enable it on to this one
        if self.frontpage:
            Exhibition.objects.all().update(frontpage=False)
        super(Exhibition, self).save()

    @permalink
    def get_absolute_url(self):
        return 'exhibition-single', (), {'year': self.start_date.strftime("%Y"), 'slug': self.slug}

    def clean(self):
        if self.frontpage:
            if not self.frontpage_uploaded_image and not self.frontpage_selected_image:
                raise ValidationError("Either upload or specify a frontpage image.")

        else:
            try:
                Exhibition.objects.exclude(pk=self.pk).get(frontpage=True)
            except Exhibition.DoesNotExist:
                raise ValidationError("Enable a different exhibition to change the frontpage.")

        if self.start_date >= self.end_date:
            raise ValidationError("The start date must be after the end date.")

    def frontpage_image(self):
        if self.frontpage_uploaded_image:
            return self.frontpage_uploaded_image
        elif self.frontpage_selected_image:
            return self.frontpage_selected_image.image
        else:
            raise ValidationError("Either upload or specify a frontpage image.")


class ExhibitionPhoto(models.Model):
    def image_path(instance, filename):
        return os.path.join(
            'exhibitions',
            str(instance.exhibition.start_date.year),
            str(instance.exhibition.name),
            filename
           )

    exhibition = models.ForeignKey(Exhibition)
    image = models.ImageField(upload_to=image_path)
    caption = models.CharField(max_length=50)
    position = models.PositiveSmallIntegerField("Position")

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return '%s from %s id: %s' % (self.caption, self.exhibition, self.id)
