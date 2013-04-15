from django.views.generic import DetailView, ListView

from .models import Press


class PressDetail(DetailView):
    model = Press


class PressList(ListView):
    model = Press
    context_object_name = 'press_list'
