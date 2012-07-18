from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Exhibition


class ExhibitionDetail(DetailView):
    def get_object(self):
        return get_object_or_404(Exhibition,
                                 start_date__year=int(self.kwargs['year']),
                                 slug=self.kwargs['slug'])
