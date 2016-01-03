from django.views.generic import DetailView

from .models import Book
from libs.common.views import ObjectList


class BookList(ObjectList):
    model = Book


class BookDetail(DetailView):
    model = Book
