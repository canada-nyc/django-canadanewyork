import subprocess

from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    LESS_SOURCE = "static/styles/main.less"
    SASS_SOURCE_DIRECTORY = "static/styles/"
    SASS_SOURCE = SASS_SOURCE_DIRECTORY + "magnific-popup.scss"
    STYLE_DESTINATION = "static/compressed/global.css"

    def handle(self, *args, **options):
        self.call_shell_command(
            'lessc --compress {} | cat - {} | sass --scss --stdin --trace --style nested --load-path {} {}'.format(
                self.LESS_SOURCE,
                self.SASS_SOURCE,
                self.SASS_DIRECTORY,
                self.STYLE_DESTINATION
            ),
        )
        print 'python manage.py collectstatic --noinput'
        call_command('collectstatic', interactive=False)

    @staticmethod
    def call_shell_command(command):
        print command
        subprocess.call(command, shell=True)
