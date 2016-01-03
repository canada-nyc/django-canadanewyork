from django_fake_model import models as f

from libs.ckeditor.fields import CKEditorField


class CKEditorModel(f.FakeModel):
    html = CKEditorField(blank=True)
