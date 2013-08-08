from .models import Book
from libs.common.views import ObjectList


class BookList(ObjectList):
    model = Book
