from django.contrib import admin
from django import forms
from canada.exhibitions.models import Exhibition, ExhibitionPhoto


class ExhibitionPhotoForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)


class ExhibitionPhotoInline(admin.TabularInline):
    model = ExhibitionPhoto
    form = ExhibitionPhotoForm
    sortable_field_name = "position"


class ExhibitionAdmin(admin.ModelAdmin):
    inlines = [ExhibitionPhotoInline]
    fieldsets = (
        (None, {
            'fields': ('name',
                       'description',
                       'artists',
                       ('start_date', 'end_date'))
        }),
        ('Frontpage', {
            'fields': ('frontpage',
                       'frontpage_uploaded_image',
                       'frontpage_selected_image',
                       'frontpage_text')
        }),
   )
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'frontpage')

admin.site.register(Exhibition, ExhibitionAdmin)
