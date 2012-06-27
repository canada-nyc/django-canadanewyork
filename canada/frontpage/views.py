from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from canada.exhibitions.models import Exhibition


def frontpage_exhibition(request):
    try:
        exhibition = Exhibition.objects.get(frontpage=True)
        context = {
            'image_size': settings.CANADA_FRONTPAGE_IMAGE_SIZE,
            'exhibition': exhibition
        }
    except ObjectDoesNotExist:
        context = {
            'image_size': settings.CANADA_FRONTPAGE_IMAGE_SIZE,
        }

    return render(request, 'index.html', context)
