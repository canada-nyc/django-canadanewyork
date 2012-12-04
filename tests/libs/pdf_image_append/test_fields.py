import pdfminer.pdfparser

from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
from django.test.utils import override_settings
from django.conf import settings

from .models import PDFImageModel
from ...common.functions import django_image


def page_count(pdf):
    '''
    returns the number of pages in the pdf file.

    ex:
    pdf_file = open(file_name, 'rb')
    print page_count(pdf_file)
    '''
    parser = pdfminer.pdfparser.PDFParser(pdf)
    doc = pdfminer.pdfparser.PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    pages = [_ for _ in doc.get_pages()]
    return len(pages)


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.libs.pdf_image_append',))
class TestContentRedirects(TestCase):
    def setUp(self):
        loading.cache.loaded = False
        call_command('syncdb', interactive=False)

    def test_create(self):
        _PDFImageModel = PDFImageModel()
        _PDFImageModel.image_append = django_image('test')
        _PDFImageModel.save()

        _PDFImageModel = PDFImageModel.objects.all()[0]
        self.assertFalse(_PDFImageModel.image_append)
        self.assertTrue(_PDFImageModel.pdf)
        self.assertEqual(1, page_count(_PDFImageModel.pdf))

    def test_append(self):
        _PDFImageModel = PDFImageModel()
        _PDFImageModel.image_append = django_image('test')
        _PDFImageModel.save()

        _PDFImageModel = PDFImageModel.objects.all()[0]
        _PDFImageModel.image_append = django_image('test2')
        _PDFImageModel.save()

        self.assertFalse(_PDFImageModel.image_append)
        self.assertTrue(_PDFImageModel.pdf)
        self.assertEqual(2, page_count(_PDFImageModel.pdf))

    def test_blank(self):
        _PDFImageModel = PDFImageModel()
        _PDFImageModel.save()

        self.assertFalse(_PDFImageModel.image_append)
        self.assertFalse(_PDFImageModel.pdf)
