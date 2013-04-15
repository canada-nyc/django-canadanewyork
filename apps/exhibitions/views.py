from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.flatpages.models import FlatPage

from .models import Exhibition


class ExhibitionList(ListView):
    queryset = Exhibition.objects.all()


class ExhibitionDetail(DetailView):
    def get_object(self):
        return get_object_or_404(
            Exhibition.objects.prefetch_related('artists', 'photos'),
            slug=self.kwargs['slug']
        )


class ExhibitionPressList(DetailView):
    template_name = 'press/press_list.html'

    def get_object(self):
        return get_object_or_404(
            Exhibition.objects.only('name').prefetch_related('press'),
            slug=self.kwargs['slug']
        )


class ExhibitionCurrent(DetailView):
    template_name = 'exhibitions/exhibition_current.html'

    def get_object(self):
        return Exhibition.objects.get_current()

    def get_context_data(self, **kwargs):
        context = super(ExhibitionCurrent, self).get_context_data(**kwargs)
        context['press_release_photo'] = context['exhibition'].get_press_release_photo()
        try:
            context['flatpage'] = FlatPage.objects.get(url__exact='/')
        except FlatPage.DoesNotExist:
            pass
        return context
