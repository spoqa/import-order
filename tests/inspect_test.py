from pytest import raises
from import_order.inspect import debug_import_names, inspect_order


def test_inspect_order_raise_without_local_packages():
    with raises(ValueError):
        inspect_order(['.'], False)


def test_debug_import_names():
    debug_names = debug_import_names(
        [('re', 0, 0, False), ('datetime', 0, 0, False)],
        ['import_order'],
        ('re', 0, 0, False)
    )
    fmt = '\x1b[30m{0}\x1b[39m \x1b[37m({1})\x1b[39m'.format(
        'datetime', '1,0,datetime,2,2,datetime'
    )
    hfmt = '\x1b[35m{0}\x1b[39m \x1b[37m({1})\x1b[39m'.format(
        're', '1,0,re,2,2,re'
    )
    assert debug_names == ', '.join([hfmt, fmt])
