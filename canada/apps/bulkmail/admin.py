from django.contrib import admin
from django.core import mail
from django.template.loader import get_template
from django.template import Context

from .models import ContactList, Contact, Message
from ..admin import image_file


def send_message(self, request, queryset):
    connection = mail.get_connection()
    connection.open()
    for message in queryset:
        subject = message.subject
        from_email = 'saul.shanabrook@gmail.com'
        for recipient in message.contact_list.contacts.all():
            context = {
                'message': message,
                'recipient': recipient,
            }
            text_content = get_template('bulkmail/message.txt').render(Context(context))
            html_content = get_template('bulkmail/message.html').render(Context(context))
            msg = mail.EmailMultiAlternatives(subject, text_content, from_email,
                                              to=[recipient.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    connection.close()


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact_list')


class ContactInline(admin.TabularInline):
    model = Contact


class ContactListAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    list_display = ('name', 'default')


class MessageAdmin(admin.ModelAdmin):
    actions = [send_message]
    list_display = ('image_thumb', 'subject', 'contact_list', 'date_time')
    list_filter = ('contact_list',)
    image_thumb = image_file('obj.image')

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactList, ContactListAdmin)
admin.site.register(Message, MessageAdmin)
