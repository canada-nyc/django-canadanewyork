from invoke import ctask as task


@task
def dev(ctx):
    ctx.run('pip install -r requirements.txt')
    ctx.run('mkdir -p tmp')
    ctx.run('npm install --global --production "less" "git://github.com/mishoo/UglifyJS2.git#3bd7ca9961125b39dcd54d2182cb72bd1ca6006e"')
