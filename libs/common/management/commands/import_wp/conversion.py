import urlparse

import dateutil.parser

from apps.artists.models import Artist
from apps.exhibitions.models import Exhibition
from apps.press.models import Press
from apps.updates.models import Update
from libs.common.models import Photo
from . import helpers


def create_artist(element, all_elements):
    A = Artist(
        visible=True,
        old_path=urlparse.urlparse(element.findtext('link')).path,
    )
    title = element.findtext('title')
    try:
        A.first_name, A.last_name = title.split()
    except ValueError:
        A.last_name = title
        A.visible = False
    A.save()
    return A


def get_artist(element):
    title = element.findtext('title')
    k = {}
    try:
        k['first_name'], k['last_name'] = title.split()
    except ValueError:
        k['last_name'] = title
    return Artist.objects.get(**k)


def create_artist_resume(element, all_elements):
    A = get_artist(
        _parent_element_from_element(element, all_elements),
    )
    A.resume = helpers.html_to_markdown(
        element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
    )
    A.save()


def create_artist_press(element, all_elements):
    P = Press(
        title=element.findtext('title'),
        date=dateutil.parser.parse(element.findtext('pubDate')).date(),
        old_path=urlparse.urlparse(element.findtext('link')).path,
    )
    try:
        P = Press.objects.get(slug=P._meta.get_field('slug')._get_value(P))
    except Press.DoesNotExist:
        P.save()
    P.pdf_image_append(
        *helpers.file_from_link(element.findtext('guid'))
    )
    P.save()
    P.artists.add(
        get_artist(
            _parent_element_from_element(
                _parent_element_from_element(element, all_elements),
                all_elements,
            )
        )
    )
    P.save()
    return P


def create_artist_photo(element, all_elements):
    return _create_photo(
        element,
        get_artist(
            _parent_element_from_element(element, all_elements)
        )
    )


def create_exhibition(element, all_elements):
    E = Exhibition(
        name=element.findtext('title'),
        description=helpers.html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        ),
        old_path=urlparse.urlparse(element.findtext('link')).path,
    )
    E.start_date, E.end_date = helpers.dates_from_text(
        text=element.findtext('title'),
        year=helpers.year_from_element(element),
    )
    E.save()
    E.artists = helpers.models_from_text(
        text=E.name + E.description,
        model=Artist,
        model_function=lambda a: a.__unicode__(),
    )
    E.save()
    return E


def get_exhibition(element):
    k = {}
    k['name'] = element.findtext('title')
    k['start_date__year'] = helpers.dates_from_text(
        text=element.findtext('title'),
        year=helpers.year_from_element(element),
    )[0].year
    return Exhibition.objects.get(**k)


def create_exhibition_photo(element, all_elements):
    return _create_photo(
        element,
        get_exhibition(
            _parent_element_from_element(element, all_elements)
        ),
    )


def create_press(element, all_elements):
    P = Press(
        old_path=urlparse.urlparse(element.findtext('link')).path,
    )
    title = element.findtext('title').split(':', 1)
    try:
        P.publisher, P.title = title
    except ValueError:
        P.title = title[0]
    try:
        P = Press.objects.get(title=P.title)
    except Press.DoesNotExist:
        P.content = helpers.html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        P.date, _ = helpers.dates_from_text(
            text=P.title,
            year=helpers.year_from_element(element),
        )
        P.save()

    P.artists = helpers.models_from_text(
        text=P.content + P.title,
        model=Artist,
        model_function=lambda A: A.__unicode__(),
    )
    P.save()
    return P


def get_press(element):
    k = {}
    title = element.findtext('title').split(':', 1)
    try:
        _, k['title'] = title
    except ValueError:
        k['title'] = title[0]
    return Press.objects.get(**k)


def create_press_file(element, all_elements):
    P = get_press(
        _parent_element_from_element(element, all_elements)
    )
    P.pdf_image_append(*helpers.file_from_link(element.findtext('guid')))
    P.save()
    return P


def create_update(element, all_elements):
    U = Update(
        description=helpers.html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        ),
        old_path=urlparse.urlparse(element.findtext('link')).path,
    )
    U.save()
    # override first save value of 'now', because auto_now_add cannot be overridden
    U.post_date = dateutil.parser.parse(element.findtext('pubDate'))
    U.save()
    for link in helpers.image_links_from_html(element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')):
        P = Photo(
            title=helpers.file_from_link(link)[0],
            content_object=U
        )
        P.clean()
        P.save()
        P.image.save(*helpers.file_from_link(link))
    return U


def _parent_element_from_element(element, all_elements):
    parent_id = element.findtext('{http://wordpress.org/export/1.1/}post_parent')
    for other_element in all_elements:
        if other_element.findtext('{http://wordpress.org/export/1.1/}post_id') == parent_id:
            return other_element


def _create_photo(element, content_object):
    P = Photo(
        title=element.findtext('title'),
        caption=helpers.html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        ),
        content_object=content_object,
    )
    text = element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded').split(',', 1)
    try:
        P.title, P.caption = text
    except ValueError:
        P.title = text[0].strip() or element.findtext('title')
    P.save()
    P.image.save(
        *helpers.file_from_link(element.findtext('guid'))
    )
    return P
