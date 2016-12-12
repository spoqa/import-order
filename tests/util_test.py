from import_order.util import get_package_name, resolve_name


def test_get_package_name():
    assert get_package_name('import_order/__init__.py') == 'import_order'
    assert get_package_name('import_order/cli.py') == 'import_order.cli'

    assert get_package_name('helloworld/models/__init__.py') == \
        'helloworld.models'
    assert get_package_name('helloworld/models/post.py') == \
        'helloworld.models.post'

    assert get_package_name('./relative/__init__.py') == 'relative'
    assert get_package_name('./relative/a.py') == 'relative.a'

    assert get_package_name('../relative2/__init__.py') == 'relative2'
    assert get_package_name('../relative2/b.py') == 'relative2.b'

    assert get_package_name('../../relative3/__init__.py') == 'relative3'
    assert get_package_name('../../relative3/c.py') == 'relative3.c'


def test_resolve_name():
    assert resolve_name('.hi', 'hello') == 'hello.hi'
    assert resolve_name('..hi', 'hello.world') == 'hello.hi'
    assert resolve_name('...hi', 'hello.spoqa.world') == 'hello.hi'

    assert resolve_name('.spoqa.world', 'hello') == 'hello.spoqa.world'
    assert resolve_name('..spoqa.world', 'hello.python') == 'hello.spoqa.world'
