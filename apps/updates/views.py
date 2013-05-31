from django.views.generic import ListView

from .models import Update


def get_url(photo, size):
    return getattr(photo, '{}_image'.format(size)).url


def get_dimension(photo, size, dimension):
    return getattr(photo, '{}_image_{}'.format(size, dimension))


class UpdateList(ListView):
    queryset = Update.objects.prefetch_related('photos')

    def get_context_data(self, **kwargs):
        context = super(UpdateList, self).get_context_data(**kwargs)
        context['updates_data'] = []
        for update in context['update_list']:
            context['updates_data'].append([update, ])
            for photo in update.photos.all():
                context['updates_data'][-1].append({
                    'large_url': get_url(photo, 'large'),
                    'thumbnail_url': get_url(photo, 'thumbnail'),
                    'large_width': get_dimension(photo, 'large', 'width'),
                    'thumbnail_width': get_dimension(photo, 'thumbnail', 'width'),
                    'large_height': get_dimension(photo, 'large', 'height'),
                    'thumbnail_height': get_dimension(photo, 'thumbnail', 'height'),
                })
        return context
