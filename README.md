# import-order


CLI that check the ordering of imports. ordering follow a below rules.

1. Module order: __future__, standard libraries, site-packages, local.
1. CONSTANT_NAMES must be the first.
1. ClassNames must be the second.
1. Rest must be in alphabetical order.

## Requirements

 - [Python 2.7.x] or [Python 3.3+]

## How to install

Via pip

    $ pip install -U import-order

Or clone source code from repository and install it.

    $ git clone git://.../import_order.git
    $ cd import_order
    $ python setup.py install


## How to use

Use `import-order` to check your python codes. if you want to check your
local package named `foo` .

    $ import-order foo

in root directory of package. for more information, look around help command.

    $ import-order --help


[Python 2.7.x]: https://www.python.org/downloads/release/python-279/
[Python 3.3+]: http://www.python.org/
