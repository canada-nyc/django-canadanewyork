from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View
from django.core.urlresolvers import reverse

from .models import Info
from ..bulkmail.views import ContactCreate


class InfoContactCreate(ContactCreate):
    template_name = 'info/info_detail.html'

    def get_success_url(self):
        return reverse('contact-success', kwargs={'email': self.object.email})

    def get_context_data(self, **kwargs):
        context = {
            'info': InfoDisplay().get_object(),
        }
        context.update(kwargs)
        return super(InfoContactCreate, self).get_context_data(**context)


class InfoDisplay(DetailView):
    def get_object(self, *args, **kwargs):
        return get_object_or_404(Info, activated=True)

    def get_context_data(self, **kwargs):
        context = {
            'form': InfoContactCreate().get_form_class(),
        }
        context.update(kwargs)
        return super(InfoDisplay, self).get_context_data(**context)


class InfoDetail(View):
    def get(self, request, *args, **kwargs):
        view = InfoDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = InfoContactCreate.as_view()
        return view(request, *args, **kwargs)
