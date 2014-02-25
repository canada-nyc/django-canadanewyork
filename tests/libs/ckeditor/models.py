from django.db import models

from libs.ckeditor.fields import CKEditorField


class CKEditorModel(models.Model):
    html = CKEditorField()
