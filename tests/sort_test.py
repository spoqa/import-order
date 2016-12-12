from pytest import raises

from import_order import ImportItem
from import_order.sort import (canonical_sort_key,
                               sort_by_type, sort_import_names)


def test_sort_by_type():
    files = ['tests/mock.py']
    directories = ['.', 'tests/test_dir']
    packages = ['tests']
    arguments = files + directories + packages
    argument = sort_by_type(arguments)
    assert set(argument.files) == set(files)
    assert set(argument.local_packages) == set(packages)
    assert set(argument.directories) == set(directories)
    with raises(IOError):
        sort_by_type(['foobar/abc.py'])


def test_sort_relative_import_belower():
    local_package_names = ['hello']
    import_names = [
        ImportItem('hello.b', 'hello.b', 1, 0, False),
        ImportItem('.a', 'hello.a', 2, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_constant():
    local_package_names = ['hello']
    import_names = [
        ImportItem('.FOO', 'hello.FOO', 1, 0, True),
        ImportItem('.foo', 'hello.foo', 2, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_class_name():
    local_package_names = ['hello']
    import_names = [
        ImportItem('.FooClass', 'hello.FooClass', 1, 0, True),
        ImportItem('.foo', 'hello.foo', 2, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_all():
    local_package_names = ['hello']
    import_names = [
        ImportItem('re.compile', 're.compile', 1, 0, False),
        ImportItem('pygments.highlight', 'pygments.highlight', 2, 0, False),
        ImportItem('.FOO', 'hello.FOO', 4, 0, True),
        ImportItem('.FooClass', 'hello.FooClass', 4, 0, True),
        ImportItem('.a', 'hello.a', 4, 0, True),
        ImportItem('.foo', 'hello.foo', 4, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_relative_import():
    local_package_names = ['hello']
    import_names = [
        ('...aladin.Aladin', 'hello.aladin.Aladin', 1, 0, True),
        ('...book.Book', 'hello.book.Book', 2, 0, True),
        ('.form.BookForm', 'hello.web.admin.form.BookForm', 3, 0, True),
        ('..db.sess', 'hello.web.db.sess', 4, 0, True),
        ('..util.', 'hello.web.util.get_count', 5, 0, True),
        ('...yes24.Yes24', 'hello.yes24.Yes24', 6, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names)
    assert import_names == sorted_


def test_sort_distinguish():
    local_package_names = ['hello']
    import_names = [
        ImportItem('re.compile', 're.compile', 1, 0, False),
        ImportItem('pytest', 'pytest', 2, 0, False),
        ImportItem('pygments.highlight', 'pygments.highlight', 2, 0, True),
        ImportItem('hello.FOO', 'hello.FOO', 3, 0, False),
        ImportItem('hello.foo', 'hello.foo', 3, 0, False),
        ImportItem('.FooClass', 'hello.FooClass', 4, 0, True),
        ImportItem('.a', 'hello.a', 4, 0, True),
    ]
    sorted_ = sort_import_names(import_names, local_package_names, True)
    assert import_names == sorted_


def test_canonical_sort_key():
    # ensure re is stdlib
    actual = canonical_sort_key(
        're.compile', 're.compile', 1, 0, False, local_package_names=['hello']
    )
    assert (1, 0, 're', 2, 2, 're.compile') == actual
    # ensure pygments is site packages
    actual = canonical_sort_key(
        'pygments', 'pygments', 1, 0, False, local_package_names=['hello']
    )
    assert (2, 0, 'pygments', 2, 2, 'pygments') == actual
    # ensure hello is local packages
    actual = canonical_sort_key(
        'hello', 'hello', 1, 0, False, local_package_names=['hello']
    )
    assert (3, 0, 'hello', 2, 2, 'hello') == actual
