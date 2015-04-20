from __future__ import print_function

import ast
import re
import sys

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.agile import PythonLexer

from .listing import list_import_names, list_python_files
from .sort import canonical_sort_key, sort_import_names


IGNORE_RE = re.compile(r'#\s*((fuck|shit)\s+)*ignore\s+import\s+order|'
                       r'#\s*no\s+import\s+order',
                       re.IGNORECASE)


def debug_import_names(import_names, local_package_names, highlight=None):
    fmt = '\x1b[30m{}\x1b[39m \x1b[37m({})\x1b[39m'.format
    hfmt = '\x1b[35m{}\x1b[39m \x1b[37m({})\x1b[39m'.format
    return ', '.join(
        (hfmt if highlight in (tup, tup[0]) else fmt)(
            tup[0],
            ','.join(str(v)
                     for v in canonical_sort_key(
                         *tup, local_package_names=local_package_names))
        )
        for tup in import_names
    )


def inspect_files(local_package_names, debug):
    errored = False
    files = []
    local_package_names = {name.rstrip('/') for name in local_package_names}
    for local_package_name in local_package_names:
        files.extend(list_python_files(local_package_name))
    for filename in files:
        with open(filename) as file_:
            if IGNORE_RE.search('\n'.join(file_.readline() for _ in range(3))):
                continue
            file_.seek(0)
            tree = ast.parse(file_.read(), filename)
        import_names = list(list_import_names(tree))
        canonical_order = sort_import_names(import_names, local_package_names)
        prev_import = None
        for actual, expected in zip(import_names, canonical_order):
            if actual[0] != expected[0]:
                errored = True
                code_offset = min(expected[1], actual[1])
                code_end = max(expected[1], actual[1])
                print(
                    '\x1b[35m{}\x1b[39m:{}-{}:'.format(
                        filename, code_offset, code_end
                    ),
                    end=' ',
                    file=sys.stderr
                )
                if prev_import is None:  # first
                    print(expected[0], 'must be the first, not', actual[0],
                          file=sys.stderr)
                else:
                    print(expected[0], 'must be above than', actual[0],
                          file=sys.stderr)
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
                                             local_package_names,
                                             expected),
                          file=sys.stderr)
                    print('\x1b[31;49;1mActual order:\x1b[39;49;00m  ',
                          debug_import_names(import_names,
                                             local_package_names,
                                             actual),
                          file=sys.stderr)
                print(file=sys.stderr)
                break
            prev_import = actual

    if errored:
        raise SystemExit(1)
