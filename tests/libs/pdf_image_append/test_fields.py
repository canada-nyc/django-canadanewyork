import pdfminer.pdfparser

from django.test import TestCase
from django.db import transaction

from .models import PDFImageModel
from ...common.functions import django_image
from ...common.base_test import AddAppMixin


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


class TestPDFImageAppend(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.pdf_image_append',)

    def setUp(self):
        transaction.enter_transaction_management()
        self.TestPDFImageModel = PDFImageModel.objects.create()

    def tearDown(self):
        self.TestPDFImageModel.delete()

    def test_create(self):
        self.TestPDFImageModel.pdf_image_append(image_content=django_image('test'))

        self.assertTrue(self.TestPDFImageModel.pdf)
        self.assertEqual(1, page_count(self.TestPDFImageModel.pdf))
        transaction.commit()
        self.assertTrue(self.TestPDFImageModel.pdf)
        self.assertEqual(1, page_count(self.TestPDFImageModel.pdf))

    def test_append(self):
        self.TestPDFImageModel.pdf_image_append(image_content=django_image('test'))
        self.TestPDFImageModel.pdf_image_append(image_content=django_image('test'))

        self.assertTrue(self.TestPDFImageModel.pdf)
        self.assertEqual(2, page_count(self.TestPDFImageModel.pdf))
        transaction.commit()
        self.assertTrue(self.TestPDFImageModel.pdf)
        self.assertEqual(2, page_count(self.TestPDFImageModel.pdf))

    def test_blank(self):
        self.assertFalse(self.TestPDFImageModel.pdf)
        transaction.commit()
        self.assertFalse(self.TestPDFImageModel.pdf)
