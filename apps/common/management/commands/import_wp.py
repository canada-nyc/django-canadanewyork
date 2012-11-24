import xml.etree.ElementTree
import urlparse
from pprint import pprint as p
import dateutil.parser
import html2text
import markdown2

from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_model


class Command(BaseCommand):
    help = 'Add data from site'
    args = '(<wordpress export file>)'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Called with one argument, specifiying the path to an exported wordpress file')

        tree = xml.etree.ElementTree.parse(
            args[0],
            parser=xml.etree.ElementTree.XMLParser(encoding="UTF-8")
        )
        root = tree.getroot()[0]
        item_elements = [element for element in root if element.tag == 'item']
        item_elements.sort(key=lambda element: element.findtext('link'))
        for element in item_elements:
            if classify(element):
                app, model, field = classify(element)
                if field:
                    set_field(
                        app,
                        model,
                        field,
                        parent_kwargs=parent_kwargs(element, app, model, field),
                        field_value=value_from_field(element, app, model, field)
                    )
                else:
                    add_model(
                        app,
                        model,
                        model_kwargs=model_kwargs(element, app, model),
                    )


def classify(item_element):
    '''
    Given an item Element, it returns the app, model and field that this
    Element represents. If the Element represents a whole model, the field
    returns None
    '''
    full_url = item_element.findtext('link')
    url = urlparse.urlparse(full_url)
    path = url.path.split('/')[1:]
    if url.netloc != 'www.canadanewyork.com' or len(path) < 2:
        return None
    if path[0] == 'artists':
        if len(path) == 2:
            return ('artists', 'Artist', None)
        if len(path) == 3 and (path[2] == 'resume' or path[2] == 'resume-2'):
            return ('artists', 'Artist', 'resume')
        if path[2] == 'press' or path[2] == 'press-2':
            if len(path) == 4:
                return ('press', 'Press', None)
            return None
        if len(path) == 3 or (path[2] == 'attachment' and len(path) == 4):
            return ('artists', 'ArtistPhoto', None)
    if path[0] == 'exhibitions':
        if len(path) == 3:
            return ('exhibitions', 'Exhibition', None)
        if len(path) == 4 or (len(path) == 5 and path[3] == 'attachment'):
            return ('exhibitions', 'ExhibitionPhoto', None)
    if path[0] == 'press':
        if len(path) == 3:
            return ('press', 'Press', None)
        if len(path) == 4:
            return ('press', 'Press', 'image')
    if path[0] == 'home':
        if len(path) == 2:
            return ('frontpage', 'frontpage', None)


def model_kwargs(element, app, model):

    def dates_from_text(text, year):
        def date_from_text(text, default, return_default=False):
            try:
                date = dateutil.parser.parse(text, default=default, fuzzy=True)
            except ValueError:
                if return_default:
                    return default
            else:
                return date

        default = dateutil.parser.parse(year)

        if text.find('-') != -1:
            return [
                date_from_text(text.split('-')[-2], default, True),
                date_from_text(text.split('-')[-1], default)
            ]
        return [
            date_from_text(text, default, True),
            None
        ]

    def year_from_element(element):
        full_url = element.findtext('link')
        url = urlparse.urlparse(full_url)
        path = url.path.split('/')[1:]
        return path[1]

    def image_from_link(url):
        return url

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

    k = {}
    k['old_url'] = urlparse.urlparse(element.findtext('link')).path

    if app == 'artists' and model == 'Artist':
        try:
            k['first_name'], k['last_name'] = element.findtext('title').split()
        except ValueError:
            return None

    if app == 'exhibitions' and model == 'Exhibition':
        k['name'] = element.findtext('title')
        k['description'] = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['start_date'], k['end_date'] = dates_from_text(
            text=element.findtext('title'),
            year=year_from_element(element),
        )

    if app == 'press' and model == 'Press':
        title = element.findtext('title').split(':', 1)
        try:
            k['publisher'], k['title'] = title
        except ValueError:
            k['title'] = title[0]
        k['content'] = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )

    if model == 'ArtistPhoto' or model == 'UpdatePhoto' or model == 'ExhibitionPhoto':
        content = html_to_markdown(
            element.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
        )
        k['title'], k['caption'] = content.split('\n', 1)
        k['image'] = image_from_link(element.findtext('guid'))
        parent = retrieve_model(parent_kwargs(element, model, field=None))

    if model == 'ArtistPhoto':
        k['artist'] = parent

    if model == 'ExhibitionPhoto':
        k['exhibition'] = parent

    if model == 'UpdatePhoto':
        k['update'] == parent

    if app == 'press' and model == 'PressPhoto':
        k['image'] = image_from_link(element.findtext('guid'))
    else:
        p([app, model])
    return k


def parent_kwargs(element, app, model, field):
    return field


def value_from_field(element, app, model, field):
    pass


def retrieve_model(app, model, model_kwargs):
    Model = get_model(app, model)
    return Model.objects.get(**model_kwargs)


def add_model(app, model, model_kwargs):
    Model = get_model(app, model)
    return Model.objects.create(**model_kwargs)


def set_field(app, model, field, field_value, parent_kwargs):
    Model = get_model(app, model)
    parent = Model.objects.get(**parent_kwargs)
    setattr(parent, field, field)
    parent.save()
