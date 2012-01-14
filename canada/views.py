from django.views.generic import TemplateView


class TextView(TemplateView):

    def render_to_response(self, context, **kwargs):
        return super(TextView, self).render_to_response(context,
                        content_type='test/plain', **kwargs)
