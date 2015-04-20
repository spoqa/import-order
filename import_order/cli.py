import optparse

from .inspect import inspect_files
from .version import VERSION


parser = optparse.OptionParser(version='%prog {}'.format(VERSION))
parser.add_option('-d', '--debug', action='store_true', default=False,
                  help='Debug mode.')


def main():
    options, args = parser.parse_args()
    inspect_files(args, options.debug)
