from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Exhibition


class ExhibitionDetail(DetailView):
    def get_queryset(self):
        return get_object_or_404(Exhibition, start_date__year=self.year, name=self.name)

class ExhibitionList(ListView):
    model = Exhibition
