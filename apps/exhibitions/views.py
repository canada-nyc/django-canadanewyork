from django.views.generic import DetailView
from django.views.generic.base import TemplateView

from .models import Exhibition
from libs.common.views import ObjectList, ObjectListFromParent
from apps.custompages.models import CustomPage


class ExhibitionList(ObjectList):
    queryset = Exhibition.objects.all()


class ExhibitionDetail(DetailView):
    queryset = Exhibition.objects.prefetch_related('photos')


class ExhibitionPressList(ObjectListFromParent):
    queryset = Exhibition.objects.only('name').prefetch_related('press')

    def get_object_list_from_parent(self, exhibition):
        return exhibition.press.all()


class ExhibitionCurrent(TemplateView):
    template_name = 'exhibitions/exhibition_current.html'

    def get_context_data(self, **kwargs):
        context = super(ExhibitionCurrent, self).get_context_data(**kwargs)

        custompage = CustomPage.objects.filter(path__exact='/')
        content = custompage.values_list('content', flat=True)
        if content:
            context['extra_content'] = content[0]

        current_exhibition = Exhibition.objects.filter(current=True)
        if current_exhibition:
            context['exhibition'] = current_exhibition[0]
        return context


class ExhibitionPressRelease(DetailView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_pressrelease.html'
