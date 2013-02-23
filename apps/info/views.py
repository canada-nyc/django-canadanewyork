from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Info


class InfoDisplay(DetailView):
    def get_object(self, *args, **kwargs):
        return get_object_or_404(Info, activated=True)
