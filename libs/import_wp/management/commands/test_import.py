import csv

import requests

from django.core.management.base import BaseCommand, CommandError
from django.test import Client


class Command(BaseCommand):
    help = 'Test that imported data created redirects'
    args = '(<url csv file to test>)'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Called with one argument, specifiying the path to a url csv file')
        c = Client()
        for url in self.get_old_urls(args[0]):
            if not url:
                continue
            response = c.get(url)
            if not response.status_code in [301, 200]:
                if not requests.get('http://www.canadanewyork.com' + url).status_code == 404:
                    print url

    def get_old_urls(self, path):
        with open(path, 'rb') as csvfile:
            url_reader = csv.reader(csvfile)
            urls_have_started = False
            for row in url_reader:
                if row:
                    url = row[0]
                    if url == 'Landing Page':
                        urls_have_started = True
                    elif urls_have_started:
                            yield url
