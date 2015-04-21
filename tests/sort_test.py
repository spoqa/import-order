from import_order.sort import sort_by_type


def test_sort_by_type():
    files = ['tests/mock.py']
    directories = ['.', 'tests/test_dir']
    packages = ['tests']
    arguments = files + directories + packages
    argument = sort_by_type(arguments)
    assert set(argument.files) == set(files)
    assert set(argument.local_packages) == set(packages)
    assert set(argument.directories) == set(directories)
