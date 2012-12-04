from django.db import models

from libs.pdf_image_append.fields import PDFImageApendField


class PDFImageModel(models.Model):
    pdf = models.FileField(upload_to='tmp', blank=True, null=True)
    image_append = PDFImageApendField()
