from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Press


class PressDetail(DetailView):
    def get_object(self):
        return get_object_or_404(Press,
                                 date__year=int(self.kwargs['year']),
                                 slug=self.kwargs['slug'])
