from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Info


class InfoDetail(DetailView):
    def get_object(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            get_object_or_404(Info, pk=self.kwargs['pk'])
        return get_object_or_404(Info, activated=True)
