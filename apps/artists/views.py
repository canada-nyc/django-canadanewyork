from django.views.generic import ListView, DetailView

from .models import Artist


class ArtistList(ListView):
    queryset = Artist.in_gallery.all()


class ArtistDetail(DetailView):
    queryset = Artist.in_gallery.all()


class ArtistPressDetail(DetailView):
    queryset = Artist.in_gallery.all()
    template_name = 'press/press_list.html'


class ArtistResume(DetailView):
    queryset = Artist.in_gallery.all()
    template_name = 'artists/artist_resume.html'
