from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Exhibition
from ..views import get_press_view


class ExhibitionDetail(DetailView):
    def get_object(self):
        return get_object_or_404(Exhibition,
                                 start_date__year=int(self.kwargs['year']),
                                 slug=self.kwargs['slug'])

ExhibitionDetailPress = get_press_view(ExhibitionDetail.as_view())
