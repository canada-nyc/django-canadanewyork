from .testing import *
from .local_storage import *


#########
# LOCAL #
#########
ALLOWED_HOSTS = ['*', ]


#########
# DEBUG #
#########

DEBUG = TEMPLATE_DEBUG = True

# Toolbar

INSTALLED_APPS += (
    'debug_toolbar',
    'debug_toolbar_autoreload',
)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda _: False
}
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.version.VersionDebugPanel',

    'debug_toolbar_autoreload.AutoreloadPanel',

)

# Devserver

INSTALLED_APPS += (
    'devserver',
)
DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.cache.CacheSummaryModule',
    # 'devserver.modules.profile.LineProfilerModule',
)


#########
# CACHE #
#########

# Remove template caching

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
