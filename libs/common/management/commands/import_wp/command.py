import xml.etree.ElementTree
import textwrap

from django.core.management.base import BaseCommand, CommandError

from .classify import classify
from .conversion import (parent_from_element,
                         model_from_element,
                         field_value_from_element)


class Command(BaseCommand):
    help = 'Add data from site'
    args = '(<wordpress export file>)'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Called with one argument, specifiying the path to an exported wordpress file')

        self.log('Parsing', 0)
        tree = xml.etree.ElementTree.parse(
            args[0],
            parser=xml.etree.ElementTree.XMLParser(encoding="UTF-8")
        )
        root = tree.getroot()[0]
        self.log('Finding Items', 1)
        item_elements = [element for element in root if element.tag == 'item']
        self.log('Sorting Items', 1)

        def sort_by_url(element):
            if 'home' not in element.findtext('link'):
                return element.findtext('link')
            return element.findtext('guid')
        item_elements.sort(key=lambda element: element.findtext('link'))
        self.log('Adding Items', 0)

        added_models = []  # So that we can clean them all after.

        for element_number, element in enumerate(item_elements):
            if classify(element):
                app, model, field = classify(element)
                self.log(
                    'Adding {}.{}_{} ({} of ~{})'.format(app,
                                                         model,
                                                         field,
                                                         element_number,
                                                         len(item_elements)),
                    1
                )
                if field:
                    parent = parent_from_element(element, item_elements)
                    setattr(
                        parent,
                        *field_value_from_element(element, app, model, field)
                    )
                    parent.save()
                else:
                    added_models.append(
                        model_from_element(element, item_elements)
                    )

        # Clean all models
        map(lambda model: model.clean(), added_models)

    def log(self, string, indent=0):
        wrapper = textwrap.TextWrapper(
            drop_whitespace=False,
            replace_whitespace=False,
            initial_indent='    ' * indent,
            subsequent_indent='    ' * indent,
            width=170,
        )
        self.stdout.write(wrapper.fill(string) + '\n')
