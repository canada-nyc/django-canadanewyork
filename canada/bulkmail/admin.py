from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from canada.bulkmail.models import *


def send_message(modeladmin, request, queryset):
    for message in queryset:
        subject = message.subject
        from_email = 'saul.shanabrook@gmail.com'
        to_emails = []
        for contact in  message.list.contact_set.all():
            to_emails.append(contact.email)

        text_content = get_template('bulkmail/email.txt').render(Context({'message': message}))
        html_content = get_template('bulkmail/email.html').render(Context({'message': message}))
        for email in to_emails:
            msg = EmailMultiAlternatives(subject,
                                         text_content,
                                         from_email,
                                         to=[email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def preview_message(modeladmin, request, queryset):
    for message in queryset:
        return HttpResponseRedirect(message.get_absolute_url())


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'list')


class ContactInline(admin.TabularInline):
    model = Contact


class ContactListAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    list_display = ('name',)


class ContactListInline(admin.TabularInline):
    model = ContactList


class MessageAdmin(admin.ModelAdmin):
    actions = [send_message, preview_message]
    list_display = ('subject', 'list', 'date_time')
    list_filter = ('list',)
    #inlines = [ContactListInline]

admin.site.register(Message, MessageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactList, ContactListAdmin)
