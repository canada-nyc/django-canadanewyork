
class NONE(object):
    def __nonzero__(self):
        return False
NONE = NONE()

class BaseAppManager(object):
    def __init__(self, context):
        '''
        ``context`` should be Invoke Context. Or any dictionary that looks like
        this:


        {
            'default_app_label': '<one of the app labels>', # Optional
            'apps': {
                '<app label>': {
                    'type': '<some type>'
                },
                '<another app label>': {
                    'type': '<some other type>',
                    '<attribute of that app>': '<value of attribute>'
                }
            }
        })
        '''
        self.default_app_label = context.get('default_app_label', NONE)

        # Get apps dictionary from config
        try:
            self.apps = context['apps']
        except KeyError:
            raise ValueError(
                'The configuration has no `apps` key. Make sure to '
                'congire the Invoke Context with a key called `apps`'
            )

        # If supplied a default app label, check if that is a proper app
        if self.default_app_label != NONE:
            try:
                self.apps[self.default_app_label]
            except KeyError:
                raise ValueError(
                    'The default app label, "{}", is not in the config. '
                    'Possible app labels are {}'.format(
                        repr(self.default_app_label),
                        str(self.apps.keys())
                    )
                )

    def get_app_label(self, app_label):
        if not app_label:
            if self.default_app_label:
                return self.default_app_label
            else:
                raise ValueError(
                    'No app label and no default app label in context'
                )
        return app_label


class SingleAppManager(object):
    def __init__(self, context):
        '''
        ``context`` should be Invoke Context. Or any dictionary that looks like
        this:


        {
            'default_app_label': '<one of the app labels>', # Optional
            'apps': {
                '<app label>': {
                    'type': '<some type>'
                },
                '<another app label>': {
                    'type': '<some other type>',
                    '<attribute of that app>': '<value of attribute>'
                }
            }
        })
        '''
        self.default_app_label = context.get('default_app_label', NONE)

        # Get apps dictionary from config
        try:
            self.apps = context['apps']
        except KeyError:
            raise ValueError(
                'The configuration has no `apps` key. Make sure to '
                'congire the Invoke Context with a key called `apps`'
            )

        # If supplied a default app label, check if that is a proper app
        if self.default_app_label != NONE:
            try:
                self.apps[self.default_app_label]
            except KeyError:
                raise ValueError(
                    'The default app label, "{}", is not in the config. '
                    'Possible app labels are {}'.format(
                        repr(self.default_app_label),
                        str(self.apps.keys())
                    )
                )

    def get_app_label(self, app_label):
        if not app_label:
            if self.default_app_label:
                return self.default_app_label
            else:
                raise ValueError(
                    'No app label and no default app label in context'
                )
        return app_label

class DoubleAppManager(object):
    '''
    Provides a nice friendly wrapper for applcation environments, when using Invoke.
    It assumes you configuring Invoke with a Context.

    It is grounded on the idea that you want to specify that target app for
    every task you call. For instance, you might want to reset the database
    on your local development environment, on your testing Heroku app, or on
    your production Heorku app. Each of these is defined in the Invoke Context,
    with a label that you use on the command line. For example:

        {
            'default_app_label': 'local',
            'apps': {
                'local': {
                    'type': 'local',
                },
                'heroku-dev': {
                    'type': 'heroku',
                    'name': 'canada-dev',
                },
                'heroku-prod': {
                    'type': 'heroku',
                    'name': 'canada'
                }
            }
        }

    This class is made to ingest a dictionary of all application environment
    and then one or two labels that correspond to different invironments.

    It is meant to be passed in a Invoke Context, but really be passed in any
    dictionary as long as it conforms to this style:

    {
        'default_app_label': '<one of the app labels>', # Optional
        'apps': {
            '<app label>': {
                'type': '<some type>'
            },
            '<another app label>': {
                'type': '<some other type>',
                '<attribute of that app>': '<value of attribute>'
            }
        }
    })

    The you can pass in an app label and it will return a nice object that has
    that has a type attribute, and any other attribtues that that label is defined
    to have. So why not just use a dictionary? Well it some nicer error handling,
    it will list all possible apps if you pass in a nonexistant one. Also if you
    pass in a false app, it will use the default if provided.

    Its real use is if you pass in two apps. Then it will assume you are
    doing a source to destination sort of thing. So it will assume the first
    app label is the source app and the second is the destination.

    Then instead of returning an object that has attributes for each dictionary key
    for the app, it will have a ``source`` and ``destination`` atributes that
    each return an object for that app, with the proper attributes on it.
    '''

    def __init__(self, context):
        '''
        ``context`` should be Invoke Context. Or any dictionary that looks like
        this:


        {
            'default_app_label': '<one of the app labels>', # Optional
            'apps': {
                '<app label>': {
                    'type': '<some type>'
                },
                '<another app label>': {
                    'type': '<some other type>',
                    '<attribute of that app>': '<value of attribute>'
                }
            }
        })
        '''
        self.default_app_label = context.get('default_app_label', NONE)

        # Get apps dictionary from config
        try:
            self.apps = context['apps']
        except KeyError:
            raise ValueError(
                'The configuration has no `apps` key. Make sure to '
                'congire the Invoke Context with a key called `apps`'
            )

        # If supplied a default app label, check if that is a proper app
        if self.default_app_label != NONE:
            try:
                self.apps[self.default_app_label]
            except KeyError:
                raise ValueError(
                    'The default app label, "{}", is not in the config. '
                    'Possible app labels are {}'.format(
                        repr(self.default_app_label),
                        str(self.apps.keys())
                    )
                )

    def __call__(self, first_app_label, second_app_label=NONE):
        if second_app_label == NONE:
            return self.get_app(first_app_label)
        else:
            self.both = self.get_two_apps([first_app_label, second_app_label])
            self.source, self.destination = self.both
            return self

    def get_app_label(self, app_label):
        if not app_label:
            if self.default_app_label:
                return self.default_app_label
            else:
                raise ValueError(
                    'No app label and no default app label in context'
                )
        return app_label

    def get_app(self, app_label):
        try:
            app = self.apps[self.get_app_label(app_label)]
        except KeyError:
            raise ValueError(
                'app label, "{}", is not in the config. Possible '
                'app labels are {}'.format(
                    repr(app_label),
                    str(self.apps.keys())
                )
            )
        return App(app)

    def get_two_apps(self, first_app_label, second_app_label):
        apps = map(self.get_app, [first_app_label, second_app_label])
        app_labels = map(lambda app: app.label, apps)
        if app_labels[0] == app_labels[1]:
            raise ValueError(
                'Both apps are "{}". Must pass in two different apps'.format(
                    app_labels[0]
                )
            )
        return apps


class App(object):
    def __init__(self, app_config):
        for key, value in app_config.items():
            setattr(self, key, value)
