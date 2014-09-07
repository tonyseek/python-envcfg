|Build Status| |PyPI Version| |PyPI Downloads| |Wheel Status|

python-envcfg
=============

Accessing environment variables with a magic module.

::

    >>> import os
    >>> from envcfg.raw.python import CONFIGURE_OPTS
    >>>
    >>> CONFIGURE_OPTS
    '--enable-shared --enable-universalsdk=/ --with-universal-archs=intel'
    >>> CONFIGURE_OPTS == os.environ['PYTHON_CONFIGURE_OPTS']
    True

It works with many frameworks such as Django and Flask. Then you can store your
config in the environment variables instead of framework-specific config files.
It is recommended by 12-Factor_.


Installation
------------

::
    $ pip install envcfg
    $ pip freeze > requirements.txt  # http://nvie.com/posts/pin-your-packages/


Issues
------

If you want to report bugs or request features, please create issues on
`GitHub Issues <https://github.com/tonyseek/python-envcfg/issues>`_.


.. _12-Factor: http://12factor.net

.. |Build Status| image:: https://travis-ci.org/tonyseek/python-envcfg.svg?branch=master,develop
   :target: https://travis-ci.org/tonyseek/python-envcfg
   :alt: Build Status
.. |Wheel Status| image:: https://pypip.in/wheel/python-envcfg/badge.svg
   :target: https://warehouse.python.org/project/python-envcfg
   :alt: Wheel Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/python-envcfg.svg
   :target: https://pypi.python.org/pypi/python-envcfg
   :alt: PyPI Version
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/python-envcfg.svg
   :target: https://pypi.python.org/pypi/python-envcfg
   :alt: Downloads
