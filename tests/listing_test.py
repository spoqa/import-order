import os

from import_order.listing import list_all_argument, list_exclude_filter
from import_order.sort import sort_by_type


def test_list_exclude_filiter():
    files = list_all_argument(sort_by_type(['tests']))
    assert list_exclude_filter(files, ['.']) == []
    assert list_exclude_filter(files, ['tests']) == []
    assert list_exclude_filter(files, ['tests/']) == []
    assert list_exclude_filter(files, ['tests/.']) == []
    assert list_exclude_filter(files, ['tests/../tests']) == []
    assert list_exclude_filter(files, [os.path.abspath('.')]) == []
    assert list_exclude_filter(files, [os.path.abspath('tests')]) == []

    assert 'tests/mock.py' in list_exclude_filter(files, [])
    result = set(files)
    result.remove('tests/mock.py')
    result_rel = set(list_exclude_filter(files, ['tests/mock.py']))
    assert result == result_rel
    result_abs = set(list_exclude_filter(files,
                                         [os.path.abspath('tests/mock.py')]))
    assert result == result_abs
