from sorl.thumbnail import get_thumbnail
from django.conf import settings


def image_file(image, short_description='Image'):
    def image_thumb(self, obj):
        image = eval(image_thumb.image)
        if image:
            thumb = get_thumbnail(image.file, settings.CANADA_ADMIN_THUMBS_SIZE)
            return u'<img width="{}" height={} src="{}" />'.format(thumb.width,
                                                                   thumb.height,
                                                                   thumb.url)
        else:
            return "No Image"

    image_thumb.__dict__.update({'short_description': short_description,
                                 'allow_tags': True,
                                 'image': image})
    return image_thumb
