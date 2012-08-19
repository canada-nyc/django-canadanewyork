from django.views.generic import View

from press.views import PressList


def get_press_view(OtherView):
    class BasePressDetail(View):
        def get(self, request, *args, **kwargs):
            view = OtherView(request, *args, **kwargs)
            if self.kwargs['press']:
                extra_context = view.context_data
                view = PressList.as_view()(request, *args, **kwargs)
                view.context_data.update(extra_context)
            return view
    return BasePressDetail
