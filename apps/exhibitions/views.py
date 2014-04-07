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

        try:
            custompage = CustomPage.objects.get(path__exact='/')
        except CustomPage.DoesNotExist:
            context['extra_content'] = ''
        else:
            context['extra_content'] = custompage.content.as_html

        try:
            current_exhibition = Exhibition.objects.get(current=True)
        except Exhibition.DoesNotExist:
            context['exhibition'] = None
        else:
            context['exhibition'] = current_exhibition

        return context


class ExhibitionPressRelease(DetailView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_pressrelease.html'
