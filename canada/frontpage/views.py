from django.shortcuts import get_object_or_404, render
from django.conf import settings

from exhibitions.models import Exhibition


def frontpage_exhibition(request):
    exhibition = get_object_or_404(Exhibition, frontpage=True)
    context = {
        'image_size': settings.CANADA_FRONTPAGE_IMAGE_SIZE,
        'exhibition': exhibition
    }
    return render(request, 'index.html', context)
