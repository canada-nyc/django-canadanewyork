from django.views.generic import ListView

from .models import Update


class UpdateListView(ListView):
    model = Update
