import urlparse
import dateutil.parser

import url_tracker

from apps.artists.models import Artist
from apps.exhibitions.models import Exhibition
from apps.press.models import Press
from apps.updates.models import Update
from apps.photos.models import Photo
from . import helpers


def create_artist(element, all_elements):
    A = Artist(visible=True)
    title = element.findtext('title')
    try:
        A.first_name, A.last_name = title.split()
    except ValueError:
        A.last_name = title
        A.visible = False
    A.save()
    url_tracker.change_urls(
        old_url=helpers.url_path(element),
        absolute_url_method='get_absolute_url',
        instance=A)
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
    )
    try:
        P = Press.objects.get(slug=P._meta.get_field('slug')._get_value(P))
    except Press.DoesNotExist:
        P.save()
    P.content_file.save(*_press_file_from_link(P, element.findtext('guid')))
    P.old_content_path = urlparse.urlparse(element.findtext('guid')).path
    P.save()
    P.artists.add(
        get_artist(
            _parent_element_from_element(
                _parent_element_from_element(
                    element,
                    all_elements
                ),
                all_elements,
            )
        )
    )
    P.save()
    url_tracker.change_urls(
        old_url=helpers.url_path(element),
        absolute_url_method='get_absolute_url',
        instance=P)
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
    url_tracker.change_urls(
        old_url=helpers.url_path(element),
        absolute_url_method='get_absolute_url',
        instance=E)
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
    P = Press()
    title = element.findtext('title').split(':', 1)
    try:
        P.publisher, P.title = title
    except ValueError:
        P.title = title[0]
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
    url_tracker.change_urls(
        old_url=helpers.url_path(element),
        absolute_url_method='get_absolute_url',
        instance=P)
    return P


def get_press(element):
    P = Press()
    title = element.findtext('title').split(':', 1)
    try:
        P.publisher, P.title = title
    except ValueError:
        P.title = title[0]
    P.content = helpers.html_to_markdown(
        element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
    )
    P.date, _ = helpers.dates_from_text(
        text=P.title,
        year=helpers.year_from_element(element),
    )
    return Press.objects.get(slug=P._meta.get_field('slug')._get_value(P), date__year=P.date.year)


def create_press_file(element, all_elements):
    P = get_press(
        _parent_element_from_element(element, all_elements)
    )
    P.content_file.save(*_press_file_from_link(P, element.findtext('guid')))
    P.save()
    url_tracker.change_urls(
        old_url=helpers.url_path(url_text=element.findtext('guid')),
        absolute_url_method='get_content_file_url',
        instance=P)
    return P


def create_update(element, all_elements):
    U = Update(
        description=helpers.html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
    )
    U.save()
    # override first save value of 'now', because auto_now_add cannot be overridden
    U.post_date = dateutil.parser.parse(element.findtext('pubDate'))
    U.save()
    for link in helpers.image_links_from_html(element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')):
        P = Photo(
            content_object=U,
        )
        P.clean()
        P.save()
        P.image.save(*helpers.file_from_link(link))
        url_tracker.change_urls(
            old_url=helpers.url_path(url_text=link),
            absolute_url_method='get_image_url',
            instance=P)
    url_tracker.change_urls(
        old_url=helpers.url_path(element),
        absolute_url_method='get_absolute_url',
        instance=U)
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
    url_tracker.change_urls(
        old_url=helpers.url_path(element),
        absolute_url_method='get_image_url',
        instance=P)
    return P


def _press_file_from_link(Press, url):
    #from pudb import set_trace; set_trace()
    if url.endswith('.jpg'):
        name, content_file = helpers.pdf_from_link(url)
        if Press.content_file:
            content_file = helpers.merge_pdfs(
                [Press.content_file.file, content_file.file]
            )
        return name, content_file
    else:
        return helpers.file_from_link(url)
