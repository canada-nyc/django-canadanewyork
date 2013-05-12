import textwrap
import pprint
import os


class Log(object):

    def __init__(self):
        self.level = 0

    def __iadd__(self, other):
        self.level += other
        return self

    def __isub__(self, other):
        self.level -= other
        return self

    def __call__(self, string):
        rows, columns = os.popen('stty size').read().split()
        width = int(columns) - 4 * self.level - 2

        if not isinstance(string, basestring):
            string = pprint.pformat(string, width=width)
        wrapper = textwrap.TextWrapper(
            initial_indent='    ' * self.level,
            subsequent_indent='    ' * self.level + '  ',
            width=width,
        )
        print wrapper.fill(string)
