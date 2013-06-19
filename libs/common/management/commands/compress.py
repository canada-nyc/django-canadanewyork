import subprocess

from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    SCRIPT_SOURCE = ' '.join([
        "static/scripts/jquery.js",
        "static/scripts/jquery.imagesloaded.js",
        "static/scripts/swipe.js",
        "static/scripts/main.js",
        "static/scripts/templates.js",
        "static/scripts/store.js",
        "static/scripts/lightbox.js",
        "static/scripts/html5shiv.min.js"
    ])
    SCRIPT_DESTINATION = "static/compressed/global.js"
    STYLE_SOURCE = "static/styles/main.less"
    STYLE_DESTINATION = "static/compressed/global.css"

    def handle(self, *args, **options):
        self.call_shell_command(
            'uglifyjs {} -o {}'.format(
                self.SCRIPT_SOURCE,
                self.SCRIPT_DESTINATION
            ),
        )
        self.call_shell_command(
            'lessc --compress {} {}'.format(
                self.STYLE_SOURCE,
                self.STYLE_DESTINATION
            ),
        )
        print 'python manage.py collectstatic --noinput'
        call_command('collectstatic', interactive=False)

    @staticmethod
    def call_shell_command(command):
        print command
        subprocess.call(command, shell=True)
