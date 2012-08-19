from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View
from pprint import pprint

from .models import Exhibition
from ..press.views import PressList


class ExhibitionDetail(DetailView):
    def get_object(self):
        return get_object_or_404(Exhibition,
                                 start_date__year=int(self.kwargs['year']),
                                 slug=self.kwargs['slug'])


class ExhibitionDetailPress(View):
    def get(self, request, *args, **kwargs):
        view = ExhibitionDetail.as_view()(request, *args, **kwargs)
        if self.kwargs['press']:
            exhibition_context = view.context_data
            view = PressList.as_view()(request, *args, **kwargs)
            view.context_data.update(exhibition_context)
        return view
