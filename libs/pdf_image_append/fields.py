from io import BytesIO

import pdfrw
import reportlab.pdfgen

from django.db.models.fields.files import ImageField
from django.core.exceptions import FieldError

from south.modelsinspector import introspector


DEFAULT_PDF_FIELD = 'pdf'


class PDFImageApendField(ImageField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        self.pdf_field = kwargs.pop('pdf_field', DEFAULT_PDF_FIELD)
        super(PDFImageApendField, self).__init__(*args, **kwargs)

    @staticmethod
    def _image_to_canvas(canvas, image):
            canvas.drawImage(image, 0, 0)
            canvas.showPage()
            return canvas

    @staticmethod
    def _save_pdf(canvas, file_object):
            canvas.save()
            pdf = file_object.getvalue()
            file_object.close()
            return pdf

    @staticmethod
    def _create_canvas():
        buffer = BytesIO()
        canvas = reportlab.pdfgen.canvas.Canvas(buffer)
        return canvas, buffer

    @staticmethod
    def _canvas_from_pdf(pdf_file):
        pdf = pdfrw.PdfReader(fdata=pdf_file.read())
        pages = map(pdfrw.buildxobj.pagexobj, pdf.pages)

        canvas, buffer = _create_canvas()

        for page in pages:
            canvas.setPageSize(tuple(page.BBox[2:]))
            canvas.doForm(pdfrw.toreportlab.makerl(canvas, page))
            canvas.showPage()
        return canvas, buffer

    def pre_save(self, model_instance, add):
        try:
            getattr(model_instance, self.pdf_field)
        except AttributeError:
            raise FieldError(
                ('In model {}, field {}, the pdf_field kwarg points to an '
                 'invalid field, "{}"').format(model_instance,
                                               self.attname,
                                               self.pdf_field)
            )
        pdf_file = getattr(model_instance, self.pdf_field)
        image = getattr(model_instance, self.attname).open()
        if not image:
            return None

        if pdf_file:
            canvas, buffer = self._canvas_from_pdf(pdf_file)
            canvas = self._image_to_canvas(canvas, image)
            pdf = self._save_pdf(canvas, buffer)

        else:
            canvas, buffer = self._create_canvas()
            canvas = self._image_to_canvas(canvas, image)
            pdf = self._save_pdf(canvas, buffer)
        setattr(model_instance, self.pdf_field, pdf)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        args, kwargs = introspector(self)
        field_class = self.__class__.__module__ + "." + self.__class__.__name__
        return (field_class, args, kwargs)
