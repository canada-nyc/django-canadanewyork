from django.db import models

from libs.pdf_image_append.models import PDFImageAppendModel


class PDFImageModel(models.Model, PDFImageAppendModel):
    pdf = models.FileField(upload_to='testing/libs/pdf_image_append', blank=True, null=True)
