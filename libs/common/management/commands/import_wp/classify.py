import urlparse
import re


def classify(item_element):
    '''
    Given an item Element, it returns the app, model and field that this
    Element represents. If the Element represents a whole model, the field
    returns None
    '''
    full_url = item_element.findtext('link')
    url = urlparse.urlparse(full_url)

    url_mapping = {
        '/artists/{0}': ('artists', 'Artist', None),
        '/artists/{0}/(resume)|(resume-2)': ('artists', 'Artist', 'resume'),

        '/exhibitions/{0}': ('exhibitions', 'Exhibition', None),

        '/artists/{0}/(press)|(press-2)': ('press', 'Press', None),
        '/artists/{0}/(press)|(press-2)/{0}': ('press', 'Press', 'add_image'),
        '/press/{0}/{0}': ('press', 'Press', None),
        '/press/{0}/{0}/{0}': ('press', 'Press', 'add_image'),

        '/archives/{0}': ('updates', 'Update', None),

        '/artists/{0}/{0}': ('common', 'Photo', None),
        '/exhibitions/{0}/{0}': ('common', 'Photo', None),
        '/archives/{0}/{0}': ('common', 'Photo', None),
        '/{0}/{0}/attachment/{0}': ('common', 'Photo', None),
    }
    for path, representation in url_mapping.items():
        path += '$'
        pattern = path.format(r'[^/]*?')
        if re.match(pattern, url.path):
            return representation
