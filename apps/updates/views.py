from django.views.generic import ListView

from .models import Update


class UpdateList(ListView):
    queryset = Update.objects.prefetch_related('photos')
