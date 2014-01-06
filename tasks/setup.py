from invoke import task, run


@task
def dev():
    run('pip install -r requirements.txt')
    run('mkdir -p tmp')
    run('npm install --global --production "less" "git://github.com/mishoo/UglifyJS2.git#3bd7ca9961125b39dcd54d2182cb72bd1ca6006e"')
