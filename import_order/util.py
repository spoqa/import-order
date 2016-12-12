try:
    from importlib.util import resolve_name
except:
    def resolve_name(name, package):
        """
        https://hg.python.org/cpython/file/3.5/Lib/importlib/util.py
        and
        https://hg.python.org/cpython/file/3.5/Lib/importlib/_bootstrap.py
        """
        if not name.startswith('.'):
            return name
        elif not package:
            raise ValueError('{!r} is not a relative name '
                             '(no leading dot)'.format(name))

        level = 0

        for character in name:
            if character != '.':
                break
            level += 1

        bits = package.rsplit('.', level - 1)

        if len(bits) < level:

            raise ValueError('attempted relative import '
                             'beyond top-level package')

        base = bits[0]

        return '{}.{}'.format(base, name[level:]) if name[level:] else base


__all__ = 'get_package_name', 'resolve_name'


def get_package_name(filename):
    package_name = filename\
        .replace('.py', '')\
        .replace('__init__', '')\
        .replace('/', '.')
    while package_name.startswith('.'):
        package_name = package_name[1:]
    while package_name.endswith('.'):
        package_name = package_name[:-1]

    return package_name
