from pytest import raises
from import_order.inspect import inspect_order


def test_inspect_order_raise_without_local_packages():
    with raises(ValueError):
        inspect_order(['.'], False)
