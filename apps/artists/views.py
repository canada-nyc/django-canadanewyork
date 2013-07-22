from django.views.generic import DetailView

from .models import Artist
from libs.common.views import ObjectList, ObjectListFromParent


class ArtistList(ObjectList):
    queryset = Artist.in_gallery.all()


class ArtistDetail(DetailView):
    queryset = Artist.in_gallery.prefetch_related('photos')


class ArtistPressList(ObjectListFromParent):
    queryset = Artist.in_gallery.all()

    def get_object_list_from_parent(self, artist):
        return artist.all_press


class ArtistExhibitionList(ObjectListFromParent):
    queryset = Artist.in_gallery.all()

    def get_object_list_from_parent(self, artist):
        return artist.exhibitions.all()


class ArtistBookList(ObjectListFromParent):
    queryset = Artist.in_gallery.all()

    def get_object_list_from_parent(self, artist):
        return artist.books.all()


class ArtistResume(DetailView):
    queryset = Artist.in_gallery.all()
    template_name = 'artists/artist_resume.html'
