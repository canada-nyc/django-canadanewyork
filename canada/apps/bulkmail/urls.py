from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import Message

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$', login_required(DetailView.as_view(model=Message, 
        template_name='bulkmail/message.html')),
       name='message-detail'
    ),
)
