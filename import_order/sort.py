from collections import namedtuple

import os
import re

from .listing import list_site_packages_paths


CAMEL_CASE_RE = re.compile(r'[A-Z][a-z0-9]+')
Argument = namedtuple('Argument', ['files', 'local_packages', 'directories'])


def package_type_order(future, stdlib, site, relative):
    order = 100
    if future:
        order = 0
    elif stdlib:
        order = 1
    elif site:
        order = 2
    elif not relative:
        order = 3
    return order


def condition_order(condition, relative):
    if not relative:
        order = 2
    elif not condition:
        order = 1
    else:
        order = 0
    return order


def canonical_sort_key(original_name, lineno, col_offset, relative,
                       local_package_names):
    # Replace '_' (95) with '~' (128) to make it below 'z' (122)
    name = original_name.replace('_', '~')
    first_name = name.split('.', 1)[0]
    if relative:
        from_, _, variable = name.rpartition('.')
        from_ = from_.lower()
    else:
        from_ = ''
        variable = ''
    future = first_name == '~~future~~'
    local = (not first_name or
             first_name.replace('~', '_') in local_package_names)
    if future or local:
        site = False
        stdlib = False
    elif first_name in {'flaskext'}:
        # flaskext is created at runtime, and has no __file__
        site = True
        stdlib = False
    else:
        try:
            imported = __import__(first_name.replace('~', '_'))
        except ImportError as e:
            if not local_package_names:
                site = False
                stdlib = False
                local = True
            else:
                raise e
        else:
            site = getattr(
                imported,
                '__file__',
                ''
            ).startswith(tuple(list_site_packages_paths()))
            stdlib = not site
    return (
        # FIXME: refactor it to use namedtuple
        # 1. Order: __future__, standard libraries, site-packages, local
        package_type_order(future, stdlib, site, relative),
        from_ or first_name.lower(),
        # 2. CONSTANT_NAMES must be the first
        condition_order(variable.isupper(), relative),
        # 3. ClassNames must be the second
        condition_order(CAMEL_CASE_RE.search(variable), relative),
        # 4. Rest must be in alphabetical order
        name.lower()
    )


def sort_import_names(import_names, local_package_names):
    return sorted(
        import_names,
        key=lambda tup: canonical_sort_key(
            *tup,
            local_package_names=local_package_names
        )
    )


def sort_by_type(args):
    files = []
    local_packages = []
    directories = []
    for arg in {name.rstrip('/') for name in args}:
        try:
            __import__(arg)
        except (ImportError, ValueError):
            if os.path.isdir(arg):
                directories.append(arg)
            elif os.path.exists(arg):
                files.append(arg)
            else:
                raise IOError("{} dosen't exists.".format(arg))
        else:
            local_packages.append(arg)
    return Argument(files=files, local_packages=local_packages,
                    directories=directories)
