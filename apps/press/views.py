from django.views.generic import DetailView

from .models import Press


class PressDetail(DetailView):
    queryset = Press.objects.exclude(content='')
