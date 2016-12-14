from __future__ import print_function

import ast
from io import open
import re
import sys

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.agile import PythonLexer

from .filter import Exclude
from .listing import list_all_argument, list_import_names
from .sort import canonical_sort_key, sort_by_type, sort_import_names
from .util import get_package_name


IGNORE_RE = re.compile(r'#\s*((fuck|shit)\s+)*ignore\s+import\s+order|'
                       r'#\s*no\s+import\s+order',
                       re.IGNORECASE)


def debug_import_names(import_names, local_package_names, highlight=None):
    fmt = '\x1b[30m{0}\x1b[39m \x1b[37m({1})\x1b[39m'.format
    hfmt = '\x1b[35m{0}\x1b[39m \x1b[37m({1})\x1b[39m'.format
    return ', '.join(
        (hfmt if highlight in (tup, tup[0]) else fmt)(
            '{}({})'.format(tup[0], tup[1]),
            ','.join(str(v)
                     for v in canonical_sort_key(
                         *tup, local_package_names=local_package_names))
        )
        for tup in import_names
    )


def inspect_order(args, debug, only_file=False, excludes=[],
                  distinguish_from_import=False):
    argument = sort_by_type(args)
    if not argument.local_packages and not only_file:
        raise ValueError('At least 1 local package name required.')
    filters = []
    if excludes:
        filters.append(Exclude(excludes))
    files = list_all_argument(argument, filters=filters)
    errored = False
    for filename in files:
        package_name = get_package_name(filename)
        with open(filename, encoding='utf-8') as file_:
            if IGNORE_RE.search('\n'.join(file_.readline() for _ in range(3))):
                continue
            file_.seek(0)
            tree = ast.parse(file_.read(), filename)
        import_names = list(list_import_names(tree, package_name))
        canonical_order = sort_import_names(import_names,
                                            argument.local_packages,
                                            distinguish_from_import)
        prev_import = None
        for actual, expected in zip(import_names, canonical_order):
            if actual.original_name != expected.original_name:
                errored = True
                code_offset = min(expected.lineno, actual.lineno)
                code_end = max(expected.lineno, actual.lineno)
                print(
                    '\x1b[35m{0}\x1b[39m:{1}-{2}:'.format(
                        filename, code_offset, code_end
                    ),
                    end=' ',
                    file=sys.stderr
                )
                expected_name = expected.original_name
                if expected_name != expected.resolved_name:
                    expected_name = '{}({})'.format(
                        expected.original_name,
                        expected.resolved_name,
                    )
                actual_name = actual.original_name
                if actual_name != actual.resolved_name:
                    actual_name = '{}({})'.format(
                        actual.original_name,
                        actual.resolved_name,
                    )
                if prev_import is None:  # first
                    print(
                        expected_name,
                        'must be the first, not',
                        actual_name,
                        file=sys.stderr
                    )
                else:
                    print(
                        expected_name,
                        'must be above than',
                        actual_name,
                        file=sys.stderr
                    )
                lineno_cols = len(str(code_end))
                format_line = (u'{0:' + str(lineno_cols) + '} {1}').format
                with open(filename, 'rb') as file_:
                    highlighted = highlight(
                        file_.read(),
                        PythonLexer(),
                        Terminal256Formatter()
                    )
                sliced = highlighted.splitlines()[code_offset - 1:code_end]
                codelisting = '\n'.join(
                    format_line(i + code_offset, line)
                    for i, line in enumerate(sliced)
                )
                print(codelisting, file=sys.stderr)
                if debug:
                    print('\x1b[32;49;1mExpected order:\x1b[39;49;00m',
                          debug_import_names(canonical_order,
                                             argument.local_packages,
                                             expected),
                          file=sys.stderr)
                    print('\x1b[31;49;1mActual order:\x1b[39;49;00m  ',
                          debug_import_names(import_names,
                                             argument.local_packages,
                                             actual),
                          file=sys.stderr)
                print(file=sys.stderr)
                break
            prev_import = actual

    if errored:
        raise SystemExit(1)
