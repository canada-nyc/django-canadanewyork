from django.views.generic import DetailView

from .models import Artist
from ..views import get_press_view

artist_view = DetailView.as_view(queryset=Artist.in_gallery.all())
ArtistDetailPress = get_press_view(artist_view)
