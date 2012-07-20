from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404

from .forms import ContactForm
from .models import ContactList


class ContactCreate(CreateView):
    form_class = ContactForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contact_list = get_object_or_404(ContactList, default=True)
        return super(ContactCreate, self).form_valid(form)
