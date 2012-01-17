from django.views.generic.list_detail import object_detail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.flatpages.models import FlatPage
from django.forms.models import modelformset_factory


from canada.bulkmail.models import *


@login_required
def limited_object_detail(request, object_id):
    return object_detail(
        request,
        object_id,
        queryset=Message.objects.filter(),
        template_name='bulkmail/email.html',
        template_object_name='message',
       )


def bulkmail_contact(request):
    contact_flatpage = get_object_or_404(FlatPage, url='/contact/')
    ContactEmailFormSet = modelformset_factory(Contact, formset=ContactEmailForm)
    completed = ''
    if request.method == 'POST':
        formset = ContactEmailFormSet(request.POST)
        if formset.is_valid():
            contact = formset.save(commit=False)
            contact.list = get_object_or_404(ContactList, default=True)
            contact.save()
            completed = contact.email
            formset = ContactEmailFormSet()
    else:
        formset = ContactEmailFormSet()
    return render(request, 'flatpages/default.html', {
        "formset": formset,
        "flatpage": contact_flatpage,
        "completed": completed,
    })
