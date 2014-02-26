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
        'lessc --compress {} | cat - {} | sass --scss --stdin --trace --style compressed --load-path {} {}'.format(
            LESS_SOURCE,
            SASS_SOURCE,
            SASS_SOURCE_DIRECTORY,
            STYLE_DESTINATION
        ),
        pty=True
    )

namespace = Collection(compile_css)
