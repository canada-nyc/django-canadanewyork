import urlparse
import dateutil.parser
import os

import html2text
import markdown2
import requests
import requests_cache

from django.db.models.loading import get_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .classify import classify

requests_cache.configure(cache_name='wp')


def parent_from_element(element, all_elements):
    parent_id = element.findtext('{http://wordpress.org/export/1.1/}post_parent')
    for other_element in all_elements:
        if other_element.findtext('{http://wordpress.org/export/1.1/}post_id') == parent_id:
            parent = other_element
    return model_from_element(parent, all_elements, create=False)


def model_from_element(element, all_elements, create=True):
    app, model, field = classify(element)
    Model = get_model(app, model)
    model_kwargs = model_kwargs_from_element(element, app, model, all_elements)

    if create:

        field_files = {}
        for field, value in model_kwargs.items():
            # Images are set as kwargs as a tuple of (file, file_name)
            if isinstance(value, tuple) and isinstance(value[0], File):
                field_files[field] = model_kwargs.pop(field)

        model = Model()
        for field, value in model_kwargs.items():
            try:
                setattr(model, field, value)
            except ValueError:  # Raised if try to save ManyToMany before it has been saved
                try:
                    model.save()
                except:
                    import ipdb; ipdb.set_trace()
                setattr(model, field, value)
        model.save()

        for field, (file_content, file_name) in field_files.items():
            getattr(model, field).save(file_name, file_content)

    else:
        for field, value in model_kwargs.items():
            if not isinstance(value, basestring):
                del model_kwargs[field]
        model = Model.objects.get(**model_kwargs)
    return model


def field_value_from_element(element, app, model, field):
    if app == 'artists' and model == 'Artist' and field == 'resume':
        return 'resume', html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )

    elif app == 'press' and model == 'Press' and field == ('add_image', 'pdf'):
        press_file = file_from_link(element.findtext('guid'))
        import ipdb; ipdb.set_trace()


def model_kwargs_from_element(element, app, model, all_elements):
    # Keywords for model to be created
    k = {'old_path': urlparse.urlparse(element.findtext('link')).path, }

    if app == 'artists' and model == 'Artist':
        try:
            k['first_name'], k['last_name'] = element.findtext('title').split()
        except ValueError:
            k['first_name'], k['last_name'] = 'blank', element.findtext('title').split(),
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

    elif app == 'common' and model == 'Photo':
        content = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['title'], k['caption'] = content.split('\n', 1)
        k['image'] = file_from_link(element.findtext('guid'))
        k['content_object'] = parent_from_element(element, all_elements)
        del k['old_path']

    elif app == 'press' and model == 'PressPhoto':
        k['image'] = file_from_link(element.findtext('guid'))
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

    return File(img_temp), os.path.basename(url)


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
