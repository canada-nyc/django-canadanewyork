import urlparse
import dateutil.parser
import os

import html2text
import markdown2
import requests
import requests_cache

from django.db.models.loading import get_model
from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import ObjectDoesNotExist

from .classify import classify

requests_cache.configure(cache_name='wp')


def get_or_create_parent(element, all_elements, command):
    command.log('Getting or creating parent element')
    command.log_level += 1
    parent_element = get_parent_element(
        element,
        all_elements,
        command
    )
    parent_kwargs = get_model_kwargs(
        parent_element,
        all_elements=all_elements,
        command=command,
        **classify(parent_element)
    )
    parent_model = get_or_create(
        model_kwargs=parent_kwargs,
        command=command,
        **classify(parent_element)
    )
    command.log_level -= 1
    return parent_model


def get_parent_element(element, all_elements, command):
    command.log('Getting parent element')
    parent_id = element.findtext('{http://wordpress.org/export/1.1/}post_parent')
    for other_element in all_elements:
        if other_element.findtext('{http://wordpress.org/export/1.1/}post_id') == parent_id:
            return other_element


def get_or_create(app, model, model_kwargs, command, field=None):
    command.log('Trying to get or create: {}'.format(model))
    command.log_level += 1
    Model = get_model(app, model)

    # Try getting the model

    get_kwargs = model_kwargs.copy()
    for field, value in model_kwargs.items():
        # If the field isn't a string, don't try to use it to find the model

        if not isinstance(value, basestring) or field == 'old_path':
            del get_kwargs[field]
    try:
        model = Model.objects.get(**get_kwargs)
    except ObjectDoesNotExist:
        command.log('Model doesnt exist, creating model')
        # If it doesn't exist, then try to create the model...
        model = Model()
    else:
        command.log('Found existing model')
    model = set_model_fields(model, model_kwargs, command)
    command.log_level -= 1
    command.log('Model is: {}'.format(model))
    return model


def set_model_fields(model, model_kwargs, command):
    command.log('Setting fields')
    command.log_level += 1
    # Take out all the file fields, cause they can't be created with them
    field_files = {}
    field_many_to_many = {}

    for field, value in model_kwargs.items():
        # Images are set as kwargs as a tuple of (file, file_name)
        if isinstance(value, tuple) and isinstance(value[0], File):
            command.log('Found file field {}'.format(field))
            field_files[field] = model_kwargs.pop(field)

        elif isinstance(value, list) and isinstance(value[0], models.Model):
            command.log('Found many to many field {}'.format(field))
            field_many_to_many[field] = model_kwargs.pop(field)

    for field, value in model_kwargs.items():
            setattr(model, field, value)
            command.log(u'Setting {} -> {}'.format(field, value))
    command.log_level -= 1
    command.log(u'Saving model')
    model.save()
    command.log_level += 1
    # Now save the file objects
    for field, contents in field_files.items():
        command.log(u'File {} -> {}'.format(field, contents[0]))
        getattr(model, field).save(*contents)

    for field, related_list in field_many_to_many.items():
        command.log(u'Many to Many Key {}'.format(field))
        command.log_level += 1
        for related in related_list:
            command.log(u'-> {}'.format(related))
            getattr(model, field).add(related)
        command.log_level -= 1

    command.log('Finished Saving')
    command.log_level -= 1
    return model


def get_field_value(element, app, model, field):
    if app == 'artists' and model == 'Artist' and field == 'resume':
        return 'resume', html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )

    elif app == 'press' and model == 'Press' and field == ('add_image', 'pdf'):
        press_file = file_from_link(element.findtext('guid'))
        import ipdb; ipdb.set_trace()


def get_model_kwargs(element, app, model, all_elements, command, field=None):
    command.log('Getting model kwargs')
    command.log_level += 1
    # Keywords for model to be created
    k = {'old_path': urlparse.urlparse(element.findtext('link')).path, }

    if app == 'artists' and model == 'Artist':
        try:
            k['first_name'], k['last_name'] = element.findtext('title').split()
        except ValueError:
            k['first_name'], k['last_name'] = 'blank', element.findtext('title'),
        k['visible'] = True

    elif app == 'exhibitions' and model == 'Exhibition':
        k['name'] = element.findtext('title')
        k['description'] = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['start_date'], k['end_date'] = dates_from_text(
            text=element.findtext('title'),
            year=year_from_element(element),
        )
        k['artists'] = artists_from_exhibition(element, k)

    elif app == 'updates' and model == 'Update':
        k['name'] = element.findtext('title')
        k['description'] = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['post_date'] = dateutil.parser.parse(
            element.findtext('{http://wordpress.org/export/1.1/}post_date')
        )

    elif app == 'press' and model == 'Press':
        title = element.findtext('title').split(':', 1)
        try:
            k['publisher'], k['title'] = title
        except ValueError:
            k['title'] = title[0]
        k['content'] = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['artists'] = [artist_from_press(element, k), ]
        k['date'] = dateutil.parser.parse(year_from_element(element), fuzzy=True)
        if k['old_path'].startswith('/artists'):
            press_file = file_from_link(element.findtext('guid'))
            import ipdb; ipdb.set_trace()

    elif app == 'common' and model == 'Photo':
        content = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['title'], k['caption'] = content.split('\n', 1)
        k['image'] = file_from_link(element.findtext('guid'))
        k['content_object'] = get_or_create_parent(element, all_elements, command)
        del k['old_path']

    elif app == 'press' and model == 'PressPhoto':
        k['image'] = file_from_link(element.findtext('guid'))
    command.log_level -= 1

    return k


def dates_from_text(text, year):
    '''
    Given a text string such as 'Show is during January 20th - February 1 2012'
    , will try to return the two dates. If only one date found, it will return
    that date and then None.

    A string of the year is required in case one isn't found
    '''
    def date_from_text(text, default):
        '''
        given a string will try to parse a date from that string
        '''
        try:
            date = dateutil.parser.parse(text, default=default, fuzzy=True)
        except ValueError:
            return None
        else:
            return date

    default = dateutil.parser.parse(year)

    try:
        first_date = text.split('-')[-2]
        second_date = text.split('-')[-1]
    except IndexError:
        first_date = text
        second_date = ''
    return (
        date_from_text(first_date, default) or default,
        date_from_text(second_date, default),
    )


def year_from_element(element):
    full_url = element.findtext('link')
    url = urlparse.urlparse(full_url)
    path = url.path.split('/')[1:]
    return path[1]


def file_from_link(url):
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(requests.get(url).content)
    img_temp.flush()

    return os.path.basename(url), File(img_temp)


def html_to_markdown(html):
    html = html.replace('[gallery]', '')

    html = markdown2.markdown(html)
    html = html.replace('\n', '<br>')
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_links = True
    h.body_width = 0
    h.unicode_snob = True

    html = h.handle(html)
    return html


def artists_from_exhibition(element, model_kwargs):
    for artist in get_model('artists', 'Artist').objects.all():
        full_text = (model_kwargs['name'] + model_kwargs['description']).lowercase()
        if artist.__unicode__().lowercase() in full_text:
            yield artist


def artist_from_press(element, model_kwargs):
    path = model_kwargs['old_path'].split('/')[1:]
    if path[0] == 'artists':
        slug = path[1]
        return get_model('artists', 'Artist').objects.get(slug=slug)
