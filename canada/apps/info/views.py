from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from .models import Info
from ..bulkmail.views import ContactCreate


class InfoContactCreate(ContactCreate):
    template_name = 'info/info_detail.html'

    success_url = '/'

    def get_context_data(self, **kwargs):
        context = {
            'info': get_object_or_404(Info, activated=True),
        }
        context.update(kwargs)
        return super(ContactCreate, self).get_context_data(**context)


class InfoDisplay(DetailView):
    def get_object(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return get_object_or_404(Info, pk=self.kwargs['pk'])
        return get_object_or_404(Info, activated=True)

    def get_context_data(self, **kwargs):
        context = {
            'form': ContactCreate().get_form_class(),
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
