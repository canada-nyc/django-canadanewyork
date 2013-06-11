from django.views.generic import ListView, DetailView

from .models import Artist


class ArtistList(ListView):
    queryset = Artist.in_gallery.all()


class ArtistDetail(DetailView):
    queryset = Artist.in_gallery.prefetch_related('photos')


class ArtistPressList(DetailView):
    queryset = Artist.in_gallery.all()
    template_name = 'press/press_list.html'
    context_object_name = "related_object"

    def get_context_data(self, **kwargs):
        context = super(ArtistPressList, self).get_context_data(**kwargs)
        context['press_list'] = context['related_object'].all_press
        return context


class ArtistExhibitionList(DetailView):
    queryset = Artist.in_gallery.all()
    template_name = 'exhibitions/exhibition_list.html'
    context_object_name = "related_object"

    def get_context_data(self, **kwargs):
        context = super(ArtistExhibitionList, self).get_context_data(**kwargs)
        context['exhibition_list'] = context['related_object'].exhibitions.all()
        return context


class ArtistResume(DetailView):
    queryset = Artist.in_gallery.all()
    template_name = 'artists/artist_resume.html'
