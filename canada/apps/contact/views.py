from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Contact


class ContactDetail(DetailView):
    def get_object(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            get_object_or_404(Contact, pk=self.kwargs['pk'])
        return get_object_or_404(Contact, activated=True)
