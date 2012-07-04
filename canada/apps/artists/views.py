from django.shortcuts import get_object_or_404, render
from django.conf import settings

from .models import Artist


def single(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    context = {
        'image_size': settings.CANADA_SLIDER_IMAGE_SIZE,
        'artist': artist,
        }
    return render(request, 'artists/single.html', context)
