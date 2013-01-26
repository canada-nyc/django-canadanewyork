from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Exhibition


class ExhibitionList(ListView):
    queryset = Exhibition.objects.all()


class ExhibitionDetail(DetailView):
    def get_object(self):
        return get_object_or_404(Exhibition.objects.prefetch_related('artists', 'photos'),
                                 start_date__year=int(self.kwargs['year']),
                                 slug=self.kwargs['slug'])


class ExhibitionPressDetail(DetailView):
    template_name = 'press/press_list.html'

    def get_object(self):
        return get_object_or_404(
            Exhibition.objects.only('name').prefetch_related('press'),
            start_date__year=int(self.kwargs['year']),
            slug=self.kwargs['slug']
        )


class ExhibitionCurrent(DetailView):
    template_name = 'exhibitions/exhibition_current.html'

    def get_object(self):
        return get_object_or_404(
            Exhibition,
            current=True,
        )
