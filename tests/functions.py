import StringIO

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile


def django_image(name):
    thumb = Image.new('RGB', size=(10, 10,))
    # Create a file-like object to write thumb data (thumb data previously created
    # using PIL, and stored in variable 'thumb')
    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')

    # Create a new Django file-like object to be used in models as ImageField using
    # InMemoryUploadedFile.  If you look at the source in Django, a
    # SimpleUploadedFile is essentially instantiated similarly to what is shown here
    return InMemoryUploadedFile(thumb_io, None, name + '.jpg', 'image/jpeg',
                                thumb_io.len, None)
