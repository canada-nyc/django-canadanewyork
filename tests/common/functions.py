import StringIO
import random

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

INK = "red", "blue", "green", "yellow"


def django_image(name, size=10):
    thumb = Image.new('RGB', (size, size,), random.choice(INK))
    # Create a file-like object to write thumb data (thumb data previously created
    # using PIL, and stored in variable 'thumb')
    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    # Create a new Django file-like object to be used in models as ImageField using
    # InMemoryUploadedFile.  If you look at the source in Django, a
    # SimpleUploadedFile is essentially instantiated similarly to what is shown here
    return InMemoryUploadedFile(thumb_io, None, name + '.jpg', 'image/jpeg',
                                thumb_io.len, None)


def django_pdf(name, size=10):
    thumb = Image.new('RGB', (size, size,), random.choice(INK))
    # Create a file-like object to write pdf data (pdf data previously created
    # using reportlab, and stored in variable 'pdf')
    thumb_io = StringIO.StringIO()

    thumb.save(thumb_io, format='PDF', resolution=200)
    thumb_io.seek(0)
    # Create a new Django file-like object to be used in models as FileField using
    # InMemoryUploadedFile.  If you look at the source in Django, a
    # SimpleUploadedFile is essentially instantiated similarly to what is shown here
    return InMemoryUploadedFile(thumb_io, None, name + '.pdf', 'application/pdf',
                                thumb_io.len, None)
