from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Frontpage


class FrontpageDetail(DetailView):
    def get_object(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return get_object_or_404(Frontpage, pk=self.kwargs['pk'])
        return get_object_or_404(Frontpage, activated=True)