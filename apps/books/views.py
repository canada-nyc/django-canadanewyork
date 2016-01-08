from django.views.generic import DetailView

from .models import Book
from libs.common.views import ObjectList


class BookList(ObjectList):
    model = Book
    template_name = 'base/list_grid.html'


class BookDetail(DetailView):
    model = Book
