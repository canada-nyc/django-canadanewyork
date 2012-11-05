from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Add data from site'
    args = '(<wordpress export file>)'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Called with one argument, specifiying the path to an exported wordpress file')

        self.log('Using file {}'.format(args[0]))
        wordpress_export = open(args[0]).read()


        data_structure = {
            'update': {
                'requires': {
                    <category domain="category">
                    wp:status: 'published'
                }
                'fields': {
                    'title': 'title',
                    'old_url': 'link',
                    'date_created': 'pubDate' "to_date Fri, 23 Mar 2012 22:40:38 +0000"
                    'text': self.decode(content:encoded)
                }
                ''
            }

        }
        print wordpress_export

    def log(self, string):
        self.stdout.write(string + '\n')
