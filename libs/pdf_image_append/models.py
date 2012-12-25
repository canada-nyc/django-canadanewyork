from io import BytesIO

import pdfrw.buildxobj
import pdfrw.toreportlab
import reportlab.pdfgen.canvas

from django.core.files.base import ContentFile


class PDFImageAppendModel(object):

    def pdf_image_append(self, image_name='', image_content='', pdf_field='pdf'):
        pdf_file = getattr(self, pdf_field)

        if image_name.lower().endswith('.pdf'):
            pdf_file.save(image_name, image_content)

        file_buffer = BytesIO()
        canvas = reportlab.pdfgen.canvas.Canvas(file_buffer)

        if pdf_file:
            pdf = pdfrw.PdfReader(fdata=pdf_file.read())
            pages = map(pdfrw.buildxobj.pagexobj, pdf.pages)
            for page in pages:
                canvas.doForm(pdfrw.toreportlab.makerl(canvas, page))
                canvas.showPage()

            pdf_name = pdf_file.name
        else:
            pdf_name = image_name or image_content.name

        canvas.drawImage(image_content.open(), 0, 0)
        canvas.showPage()

        canvas.save()
        django_pdf = ContentFile(file_buffer.getvalue())
        file_buffer.close()

        pdf_file.save(pdf_name, django_pdf)
