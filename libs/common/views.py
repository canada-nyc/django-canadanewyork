from django.views.generic import DetailView, ListView
from .utils import select_template_name


class BaseCustomObjectList(object):
    template_name = 'base/list.html'

    def model_from_queryset(self, queryset):
        return queryset.model._meta.verbose_name_plural.capitalize()

    def list_item_template_name(self, queryset):
        model_template = "{}/{}_list_item.html".format(
            queryset.model._meta.app_label,
            queryset.model._meta.object_name.lower(),
        )
        generic_template = "base/list_item.html"
        return select_template_name([model_template, generic_template])

    def add_context_data(self, context):
        context['object_label'] = self.model_from_queryset(context['object_list'])
        context['object_list_item_template'] = self.list_item_template_name(
            queryset=context['object_list']
        )
        return context


class ObjectList(BaseCustomObjectList, ListView):
    def get_context_data(self, **kwargs):
        context = super(ObjectList, self).get_context_data(**kwargs)
        return self.add_context_data(context)


class ObjectListFromParent(BaseCustomObjectList, DetailView):

    def get_object_list_from_parent(self, parent):
        raise NotImplementedError()

    def get_context_data(self, **kwargs):
        context = super(ObjectListFromParent, self).get_context_data(**kwargs)
        context['object_list'] = self.get_object_list_from_parent(context['object'])
        context['parent_object'] = context['object']
        del context['object']
        return self.add_context_data(context)
