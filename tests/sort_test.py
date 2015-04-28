from import_order.sort import sort_by_type, sort_import_names


def test_sort_by_type():
    files = ['tests/mock.py']
    directories = ['.', 'tests/test_dir']
    packages = ['tests']
    arguments = files + directories + packages
    argument = sort_by_type(arguments)
    assert set(argument.files) == set(files)
    assert set(argument.local_packages) == set(packages)
    assert set(argument.directories) == set(directories)


def test_sort_relative_import_belower():
    local_package_names = ['hello']
    import_names = [('hello.b', 1, 0, False), ('.a', 2, 0, True)]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_
