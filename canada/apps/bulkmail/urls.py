from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.decorators import login_required

from .models import Message
from .views import ContactDelete

urlpatterns = patterns('',
    url(r'^admin/bulkmail/preview/(?P<pk>\d+)$',
        login_required(DetailView.as_view(
            model=Message,
            template_name='bulkmail/message.html')),
       name='message-detail'
    ),
    url(r'^contact/(?P<email>.*)/delete/$', ContactDelete.as_view(),
        name='contact-delete'),
    url(r'^contact/(?P<email>.*)/success/$',
        TemplateView.as_view(template_name='bulkmail/contact_add_success.html'),
        name='contact-success'
    ),
)
