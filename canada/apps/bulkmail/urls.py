from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import Message

urlpatterns = patterns('',
                       url(
                           r'^(?P<pk>\d+)$',
                           login_required(DetailView.as_view(template_name='bulkmail/email.html', model=Message,
                                                             context_object_name='message')),
                           name='message_html'
                      ),
                      )
