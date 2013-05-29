import xml.etree.ElementTree
import collections
import re

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.db import transaction

from .. import log, conversion, helpers


class Command(BaseCommand):
    help = 'Add data from site'
    args = '(<wordpress export file>), (<object number to start on>)'

    def handle(self, *args, **options):
        L = log.Log()
        if not len(args):
            raise CommandError('Called with one or two arguments, specifiying the path to an exported wordpress file and the object number to start on')

        if len(args) == 2:
            starting_number = int(args[1])
        else:
            starting_number = None
        L('Parsing')
        tree = xml.etree.ElementTree.parse(
            args[0],
            parser=xml.etree.ElementTree.XMLParser(encoding="UTF-8")
        )
        elements = tree.getroot()[0]
        L('Adding Items')
        model_create_functions = collections.OrderedDict([
            ('/artists/{0}', conversion.create_artist),
            ('/artists/{0}/(resume|resume-2)', conversion.create_artist_resume),
            ('/artists/{0}/(press|press-2)/{0}', conversion.create_artist_press),
            ('/artists/{0}/(?!(press|resume)){0}', conversion.create_artist_photo),
            ('/artists/{0}/attachment/{0}', conversion.create_artist_photo),

            ('/exhibitions/{0}/{0}', conversion.create_exhibition),
            ('/exhibitions/{0}/{0}/{0}', conversion.create_exhibition_photo),
            ('/exhibitions/{0}/{0}/attachment/{0}', conversion.create_exhibition_photo),

            ('/press/{0}/{0}', conversion.create_press),
            ('/press/{0}/{0}/attachment/{0}', conversion.create_press_file),
            ('/press/{0}/{0}/{0}', conversion.create_press_file),

            ('/archives/{0}', conversion.create_update)
        ])

        added_models = []
        L += 1
        for url_format, e_function in model_create_functions.items():
            url_format += '$'
            url_format = url_format.format(r'[^/]+?')
            L('converting {} with {}'.format(url_format, e_function.__name__))
            url_test = re.compile(url_format)
            for element in elements:
                try:
                    url = helpers.path_from_element(element)
                except AttributeError:
                    pass
                else:
                    if url_test.match(url):
                        number = len(added_models)
                        if starting_number and number < starting_number:
                            added_models.append(None)
                            continue
                        L += 1
                        L('adding #{}, {}'.format(number, url))
                        try:
                            sid = transaction.savepoint()
                            added_models.append(e_function(element, elements))
                            transaction.savepoint_commit(sid)
                        except IntegrityError:
                            transaction.savepoint_rollback(sid)
                            L += 1
                            L('Duplicate, not added')
                            L -= 1
                        L -= 1
        L -= 1

        L('Cleaning models')

        def clean_model(model):
            if model:
                # so that it will get the current DB version
                # for instance artists will have two entries, one with the
                # resume and one without. so on each it will get the real one
                model = model.__class__.objects.get(pk=model.pk)
                model.clean()
                model.save()
        # Clean all models
        map(clean_model, added_models)
