from django.views.generic import DetailView

from .models import CustomPage


class CustomPageDetail(DetailView):
    model = CustomPage

    def get_template_names(self):
        return 'custompages/' + self.request.path.strip('/') + '.html'

    def get_object(self):
        try:
            return self.get_queryset().get(path=self.request.path)
        except self.model.DoesNotExist:
            return None
