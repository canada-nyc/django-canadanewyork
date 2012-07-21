from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView
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
    url(r'^info/contact/delete/(?P<email>.*)$', ContactDelete.as_view(),
        name='contact-delete')
)
