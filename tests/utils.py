import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


def django_image(name, size=10, color='red'):
    thumb = Image.new('RGB', (size, size,), color)

    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    return SimpleUploadedFile(name, thumb_io)
