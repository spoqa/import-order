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


def test_sort_constant():
    local_package_names = ['hello']
    import_names = [('.FOO', 1, 0, True), ('.foo', 2, 0, True)]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_class_name():
    local_package_names = ['hello']
    import_names = [('.FooClass', 1, 0, True), ('.foo', 2, 0, True)]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_all():
    local_package_names = ['hello']
    import_names = [
        ('re.compile', 1, 0, False),
        ('pygments.highlight', 2, 0, False),
        ('hello.FOO', 3, 0, False),
        ('hello.foo', 3, 0, False),
        ('.FooClass', 4, 0, True),
        ('.a', 4, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_
