import xml.etree.ElementTree
import textwrap
import pprint


from django.core.management.base import BaseCommand, CommandError

from .classify import classify
from . import conversion


class Command(BaseCommand):
    help = 'Add data from site'
    args = '(<wordpress export file>)'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Called with one argument, specifiying the path to an exported wordpress file')

        self.log('Parsing')
        tree = xml.etree.ElementTree.parse(
            args[0],
            parser=xml.etree.ElementTree.XMLParser(encoding="UTF-8")
        )
        root = tree.getroot()[0]
        self.log_level += 1
        self.log('Finding Items')
        item_elements = [element for element in root if element.tag == 'item']
        self.log('Sorting Items')

        def sort_by_url(element):
            if 'home' not in element.findtext('link'):
                return element.findtext('link')
            return element.findtext('guid')
        item_elements.sort(key=lambda element: element.findtext('link'))
        self.log_level = 0
        self.log('Adding Items')

        added_models = []  # So that we can clean them all after.

        for element_number, element in enumerate(item_elements):
            self.log_level = 1
            if classify(element):
                self.log(
                    'Adding {0[0]}.{0[1]}_{0[2]} ({1} of ~{2})'.format(
                        classify(element).values(),
                        element_number,
                        len(item_elements),
                    )
                )
                self.log_level = 2
                if classify(element)['field']:
                    field_value = conversion.get_field_value(
                        element,
                        **classify(element)
                    )
                    model_kwargs = {
                        classify(element)['field']: field_value
                    }
                    parent_model = conversion.get_or_create_parent(
                        element,
                        item_elements,
                        self
                    )
                    conversion.set_model_fields(parent_model, model_kwargs, self)

                else:
                    model_kwargs = conversion.get_model_kwargs(
                        element,
                        all_elements=item_elements,
                        command=self,
                        **classify(element)
                    )
                    model = conversion.get_or_create(
                        model_kwargs=model_kwargs,
                        command=self,
                        **classify(element)
                    )
                    added_models.append(model)

        # Clean all models
        map(lambda model: model.clean(), added_models)

    @staticmethod
    def pprint(object):
        return pprint.pformat(object, width=150)

    log_level = 0

    def log(self, string):
        wrapper = textwrap.TextWrapper(
            initial_indent='    ' * self.log_level,
            subsequent_indent='     ' * self.log_level + '  ',
            width=160,
        )
        print wrapper.fill(string)
