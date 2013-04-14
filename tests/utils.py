import StringIO

from PIL import Image

from django.core.files import File


def django_image(name, size=10, color='red'):
    thumb = Image.new('RGB', (size, size,), color)

    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    return File(name, thumb_io)


def django_pdf(name, size=10):
    thumb = Image.new('RGB', (size, size,), 'red')

    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='PDF', resolution=200)
    thumb_io.seek(0)

    return File(thumb_io, name)
