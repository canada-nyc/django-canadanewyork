from django.conf import settings


def image_size(request):
    return {'image_size': settings.CANADA_IMAGE_SIZE}
