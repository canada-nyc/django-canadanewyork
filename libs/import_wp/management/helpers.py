import os
import urlparse
from StringIO import StringIO
from HTMLParser import HTMLParser

import requests
try:
    import requests_cache
except ImportError:
    pass
else:
    requests_cache.install_cache(cache_name='static/wordpress/.image_cache')
import dateutil.parser
from bs4 import BeautifulSoup
from PIL import Image
import PyPDF2

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.core.files.base import ContentFile


class TagDropper(HTMLParser):
    def __init__(self, tags_to_drop, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._text = []
        self._tags_to_drop = set(tags_to_drop)

    def clear_text(self):
        self._text = []

    def get_text(self):
        return ''.join(self._text)

    def handle_starttag(self, tag, attrs):
        if tag not in self._tags_to_drop:
            self._text.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self._text.append('</{0}>'.format(tag))

    def handle_data(self, data):
        self._text.append(data)


def path_from_url(url_text):
    url = urlparse.urlparse(url_text)
    return url.path


def path_from_element(element, field='link'):
    url_text = element.findtext(field)
    return path_from_url(url_text)


def cleanup_html(html):
    html = html.replace('[gallery]', '')
    html = html.replace('\n\n', '\n')
    html = html.replace('\n', '\n<br>')
    td = TagDropper(['img'])
    td.feed(html)
    return td.get_text()


def image_links_from_html(html):
    html = html.replace('[gallery]', '')
    soup = BeautifulSoup(html)
    for link in soup.find_all('img'):
        yield link.get('src')


def file_from_link(url):
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(requests.get(url).content)
    img_temp.flush()
    filename = os.path.basename(url)
    return filename, File(img_temp)


def image_from_link(url):
    r = requests.get(url)
    filename = os.path.basename(url)
    I = Image.open(StringIO(r.content))
    return filename, I


def pdf_from_image(image):
    thumb_io = StringIO()
    image.thumbnail((8.5 * 72, 11 * 72), Image.ANTIALIAS)
    image.save(thumb_io, format='PDF')

    return ContentFile(thumb_io.getvalue())


def merge_pdfs(pdfs):
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdfs:
        merger.append(fileobj=pdf)

    thumb_io = StringIO()
    merger.write(thumb_io)
    return ContentFile(thumb_io.getvalue())


def pdf_from_link(url):
    name, image = image_from_link(url)
    pdf = pdf_from_image(image)
    return name + '.pdf', pdf


def year_from_element(element):
    path = path_from_element(element)
    year = path.split('/')[2]
    return year


def date_from_text(text, year, default=None, return_default=False):
    '''
    given a string will try to parse a date from that string
    '''
    try:
        default = default or dateutil.parser.parse(year)
    except ValueError:
        try:
            default = dateutil.parser.parse(year.split('-')[0])
        except ValueError:
            default = dateutil.parser.parse('2013')
    for pos in range(len(text)):
        date_text = text[pos:]
        # resulting_text = text[:pos]
        resulting_text = text
        try:
            date = dateutil.parser.parse(date_text, default=default)
        except (ValueError, TypeError):
            pass
        else:
            return date, resulting_text
    if return_default:
        return default, text
    return None, text


def dates_from_text(text, year):
    '''
    Given a text string such as 'Show is during January 20th - February 1 2012'
    , will try to return the two dates and the string without the dates. If only one date found, it will return
    that date and then None.

    A string of the year is required in case one isn't found
    '''
    text_split = text.split('-', 1)
    dates = []
    if len(text_split) == 2:
        second_date, _ = date_from_text(text_split[1], year)
        dates.append(second_date)
        first_date, resulting_text = date_from_text(text_split[0], default=second_date, year=year)
        dates.append(first_date)
    else:
        first_date, resulting_text = date_from_text(text_split[0], year=year)
        dates.append(first_date)
    dates = sorted(filter(None, dates))
    dates = map(lambda date: date if len(str(date.year)) == 4 else date.replace(year=int(year)), dates)
    if len(dates) == 0:
        return dateutil.parser.parse(year), None, resulting_text
    elif len(dates) == 1:
        return dates[0], None, resulting_text
    resulting_text = text
    return dates[0], dates[1], resulting_text


def models_from_text(text, model):
    '''
    Given a model, tries to find that model in the text, using the
    model_function of the model to search the text.
    '''
    for model_instance in model.objects.all():
        if unicode(model_instance).lower() in text.lower():
            yield model_instance
