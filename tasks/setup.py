from invoke import ctask as task


@task
def python(ctx):
    '''
    Install required python packages
    '''
    print 'Setting up Python'
    ctx.run('pip install -r requirements.txt')


@task
def static(ctx):
    '''
    Install NPM modules to compress static and crates local static folder
    '''
    print 'Setting up static'
    ctx.run('mkdir -p tmp')
    ctx.run('npm install --global --production "less" "git://github.com/mishoo/UglifyJS2.git#3bd7ca9961125b39dcd54d2182cb72bd1ca6006e"')


@task
def heroku(ctx):
    '''
    Install Heroku plugins
    '''
    print 'Setting up Heroku CLI'
    ctx.run('heroku plugins:install git://github.com/saulshanabrook/heroku-config.git')
    ctx.run('heroku plugins:install git://github.com/heroku/heroku-pipeline.git')
