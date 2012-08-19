from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView

from .models import Press


class PressDetail(DetailView):
    def get_object(self):
        return get_object_or_404(Press,
                                 date__year=int(self.kwargs['year']),
                                 slug=self.kwargs['slug'])


class PressList(ListView):
    model = Press
    def get_objects(self):
        print self.get_context_data()
        if 'exhibition' in self.get_context_data():
            return get_list_or_404(Press,
                                   exhibition=self.get_context_data()['exhibition'])
