import os

from import_order.filter import Exclude
from import_order.listing import list_all_argument
from import_order.sort import sort_by_type


def test_filter_exclude():
    files = list_all_argument(sort_by_type(['tests']))

    exclude_filter = Exclude([])
    assert 'tests/mock.py' in exclude_filter.apply(files)
    exclude_filter = Exclude(['mock.py'])
    assert 'tests/mock.py' in exclude_filter.apply(files)

    exclude_filter = Exclude(['.'])
    assert exclude_filter.apply(files) == []
    exclude_filter = Exclude(['tests'])
    assert exclude_filter.apply(files) == []
    exclude_filter = Exclude(['tests/../tests'])
    assert exclude_filter.apply(files) == []
    exclude_filter = Exclude([os.path.abspath('tests')])
    assert exclude_filter.apply(files) == []

    exclude_filter = Exclude(['tests/test_dir/foo'])
    assert set(files) == set(exclude_filter.apply(files))

    files = ['tests/test_dir/foo.py', 'tests/test_dir/bar.py',
             'tests/mock.py']
    exclude_filter = Exclude(['tests/mock.py'])
    assert set(exclude_filter.apply(files)) == set(['tests/test_dir/foo.py',
                                                    'tests/test_dir/bar.py'])
    exclude_filter = Exclude(['tests/test_dir'])
    assert set(exclude_filter.apply(files)) == set(['tests/mock.py'])
    exclude_filter = Exclude(['tests/test_dir/foo.py',
                              'tests/test_dir/bar.py'])
    assert set(exclude_filter.apply(files)) == set(['tests/mock.py'])
