from django.views.generic import ListView
from django.conf import settings

from canada.updates.models import Update


class UpdateListView(ListView):
    model = Update
    context_object_name = 'updates'
    template_name = 'updates/list.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateListView, self).get_context_data(**kwargs)
        context['image_size'] = str(settings.CANADA_UPDATES_IMAGE_SIZE)
        return context
