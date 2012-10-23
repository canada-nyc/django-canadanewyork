# The post_compile hook is run by heroku-buildpack-python


echo "-----> Installing mercurial"
pip install mercurial

PATH="$HOME/bin:$PATH"
