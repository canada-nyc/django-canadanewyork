from invoke import Collection, ctask as task


LESS_SOURCE = "static/styles/main.less"
SASS_SOURCE_DIRECTORY = "static/styles/magnific"
SASS_SOURCE = "static/bower_components/magnific-popup/src/css/main.scss"
STYLE_DESTINATION = "static/compressed/global.css"


@task
def compile_css(ctx):
    '''
    Runs less and sass on the local machine.
    '''
    ctx.run(
        'lessc '
        '--compress '
        'static/styles/main.less '
        'static/compressed/main.css'
    )
    ctx.run(
        'scss '
        '--trace '
        '--style compressed '
        '--load-path static/styles/magnific '
        'static/bower_components/magnific-popup/src/css/main.scss '
        'static/compressed/magnific-popup.css'
    )

namespace = Collection(compile_css)
