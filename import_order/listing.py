import ast
import os
import os.path
import site
import sys


def list_site_packages_paths():
    site_packages_paths = set([site.USER_SITE])
    try:
        site_packages_paths.update(site.getsitepackages())
    except AttributeError:
        pass
    try:
        user_site = site.getusersitepackages()
        if isinstance(user_site, str):
            site_packages_paths.add(user_site)
        else:
            site_packages_paths.update(user_site)
    except AttributeError:
        pass
    try:
        virtualenv_path = os.environ['VIRTUAL_ENV']
    except KeyError:
        pass
    else:
        virtualenv_src_path = os.path.join(virtualenv_path, 'src')
        site_packages_paths.update(
            path
            for path in sys.path
            if path.startswith(virtualenv_path) and (
                'site-packages' in path or
                path.startswith(virtualenv_src_path)
            )
        )
    return site_packages_paths


def list_python_files(dirname):
    for entry in os.listdir(dirname):
        path = os.path.join(dirname, entry)
        if os.path.isdir(path):
            for subentry in list_python_files(path):
                yield subentry
        elif entry.endswith('.py'):
            yield path


def list_import_names(tree):
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                yield name.name, node.lineno, node.col_offset, False
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                yield ('.' * node.level +
                       (node.module + '.' if node.module else '') +
                       name.name,
                       node.lineno, node.col_offset, True)
        else:
            continue


def list_all_argument(argument, filters=[]):
    files = argument.files
    for local_package_name in argument.local_packages:
        files.extend(list_python_files(local_package_name))
    for directory in argument.directories:
        files.extend(list_python_files(directory))
    for filter_ in filters:
        files = filter_.apply(files)
    return set(files)
