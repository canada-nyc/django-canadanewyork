from django.shortcuts import get_object_or_404, render
from django.conf import settings

from artists.models import Artist


def single(request, first_name, last_name):
    artist = get_object_or_404(Artist, first_name=first_name, last_name=last_name)
    context = {
        'image_size': settings.CANADA_SLIDER_IMAGE_SIZE,
        'artist': artist,
        }
    return render(request, 'artists/single.html', context)
