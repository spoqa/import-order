import re

from .listing import list_site_packages_paths


CAMEL_CASE_RE = re.compile(r'[A-Z][a-z0-9]+')


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
    local = not first_name or first_name in local_package_names
    if future or local:
        site = False
        stdlib = False
    elif first_name in {'flaskext'}:
        # flaskext is created at runtime, and has no __file__
        site = True
        stdlib = False
    else:
        try:
            site = getattr(
                __import__(first_name.replace('~', '_')),
                '__file__',
                ''
            ).startswith(tuple(list_site_packages_paths()))
            stdlib = not site
        except ImportError:
            print(original_name)
            print(first_name)
    return (  # FIXME: refactor it to use namedtuple
              # 1. Order: __future__, standard libraries, site-packages, local
              (0 if future else (1 if stdlib else (2 if site else 3))),
              from_ or first_name.lower(),
              # 2. CONSTANT_NAMES must be the first
              not variable.isupper() if relative else None,
              # 3. ClassNames must be the second
              not CAMEL_CASE_RE.search(variable) if relative else None,
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
