import-order
==============

CLI that check the ordering of imports. ordering follow a below rules.

1. Module order: ``__future__`` , standard libraries, site-packages, local.
2. ``CONSTANT_NAMES`` must be the first.
3. ``ClassNames`` must be the second.
4. Rest must be in alphabetical order.


Requirements
--------------

- Python 2.7.x or Python 3.3+


How to install
----------------

Via pip

.. code-block::

   $ pip install -U import-order

Or clone source code from repository and install it.

.. code-block::

   $ git clone git://.../import_order.git
   $ cd import_order
   $ python setup.py install


How to use
-----------

Use ``import-order`` to check your python codes. If you want to check your
local package named ``foo`` in root directory of package.

.. code-block::

   $ import-order foo

For more information, look around help command.

.. code-block::

   $ import-order --help


Author and license
-------------------

import-order is maintained by Spoqa_, and licensed
under GPL3_ or later.


.. _GPL3: https://www.gnu.org/licenses/gpl.txt
.. _Spoqa: http://http://www.spoqa.com/
