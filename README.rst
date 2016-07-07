|Build Status| |Coverage Status| |PyPI Version| |PyPI Downloads| |Wheel Status|

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

    $ pip install python-envcfg


Supported Formats
-----------------

- ``import envcfg.raw.foo as config``:
  Import each ``FOO_*`` environment variable as string.
- ``import envcfg.json.foo as config``:
  Import each ``FOO_*`` environment variable as JSON body.
- ``import envcfg.smart.foo as config``:
  Try to import each ``FOO_*`` environment variable as JSON body, if fail then import it as string.

There is an example table:

+----------------------+---------------------------+-----------------------+
| Environment Variable | Python Import Statement   | Python Variable Value |
+======================+===========================+=======================+
| ``FOO_NAME=foo``     | ``envcfg.raw.foo.NAME``   | ``'foo'``             |
+----------------------+---------------------------+-----------------------+
| ``FOO_NAME="foo"``   | ``envcfg.raw.foo.NAME``   | ``'"foo"'``           |
+----------------------+---------------------------+-----------------------+
| ``FOO_NUM1=42``      | ``envcfg.raw.foo.NUM1``   | ``'42'``              |
+----------------------+---------------------------+-----------------------+
| ``FOO_NUM1="42"``    | ``envcfg.raw.foo.NUM1``   | ``'"42"'``            |
+----------------------+---------------------------+-----------------------+
| ``FOO_NAME=foo``     | ``envcfg.json.foo.NAME``  | *ImportError*         |
+----------------------+---------------------------+-----------------------+
| ``FOO_NAME="foo"``   | ``envcfg.json.foo.NAME``  | ``'foo'``             |
+----------------------+---------------------------+-----------------------+
| ``FOO_NUM1=42``      | ``envcfg.json.foo.NUM1``  | ``42``                |
+----------------------+---------------------------+-----------------------+
| ``FOO_NUM1="42"``    | ``envcfg.json.foo.NUM1``  | ``'42'``              |
+----------------------+---------------------------+-----------------------+
| ``FOO_NAME=foo``     | ``envcfg.smart.foo.NAME`` | ``'foo'``             |
+----------------------+---------------------------+-----------------------+
| ``FOO_NAME="foo"``   | ``envcfg.smart.foo.NAME`` | ``'foo'``             |
+----------------------+---------------------------+-----------------------+
| ``FOO_NUM1=42``      | ``envcfg.smart.foo.NUM1`` | ``42``                |
+----------------------+---------------------------+-----------------------+
| ``FOO_NUM1="42"``    | ``envcfg.smart.foo.NUM1`` | ``'42'``              |
+----------------------+---------------------------+-----------------------+

Examples
--------

Uses with Flask
~~~~~~~~~~~~~~~

1. Defines environment variables with a prefix::

    $ cat .env  # should not checked into VCS
    # values are valid JSON expressions
    MYAPP_DEBUG=true
    MYAPP_SECRET_KEY='"7950ad141c7e4b3990631fcdf9a1d909"'
    MYAPP_SQLALCHEMY_DATABASE_URI='"sqlite:///tmp/myapp.sqlite3"'

2. Creates Flask app and loads config from python-envcfg::

    $ cat myapp.py
    ...
    app = Flask(__name__)
    app.config.from_object('envcfg.json.myapp')  # MYAPP_ -> .myapp
    ...

3. Enters your app with those environment variables::

    $ env $(cat .env | xargs) python myapp.py


Uses with Django
~~~~~~~~~~~~~~~~

1. Creates a django project and moves all sensitive config items into the
   environment variables::

    $ cat djapp/settings.py  # codebase-scope config
    ...
    INSTALLED_APPS = (
        'django.contrib.admin',
    )
    ...

    $ cat .env  # environment-scope config, should not checked into VCS
    # values are valid JSON expressions
    DJAPP_SECRET_KEY='"wo9g2o#jws=u"'
    DJAPP_DEBUG=true
    DJAPP_TEMPLATE_DEBUG=true

2. Adds importing statements in the end of ``settings.py`` module::

    $ tail -n 2 djapp/settings.py
    # importing all config items stored in the environment variables 
    from envcfg.json.djapp import *  # noqa

3. Runs your Django app with environment variables::

    $ env $(cat .env | xargs) python manage.py runserver


Uses with Tornado
~~~~~~~~~~~~~~~~~

1. Defines environment variables with a prefix::

    $ cat .env
    export TORAPP_PORT='8888'
    export TORAPP_MYSQL_HOST='"127.0.0.1"'
    export TORAPP_MYSQL_DATABASE='"database"'


2. Creates a Tornado project and loads config::

    $ cat torapp/server.py

    from tornado.web import Application, RequestHandler
    from tornado.ioloop import IOLoop
    from tornado.options import define, options
    from tordb import Connection


    def options_from_object(*args, **kwargs):
        module = __import__(*args, **kwargs)
        for name, value in vars(module).items():
            name = name.lower()
            if name in options._options:
                options._options[name].set(value)


    class IndexHandler(RequestHandler):
        def initialize(self):
            self.db = Connection(options.mysql_host, options.mysql_database)

        def get(self):
            pass  # some database operations with ``self.db``


    application = Application([
        (r'/', IndexHandler),
    ])

    define('port', type=int)
    define('mysql_host', type=unicode)
    define('mysql_database', type=unicode)
    options_from_object('envcfg.json.torapp', fromlist=['torapp'])


    if __name__ == '__main__':
        application.listen(options.port)
        IOLoop.instance().start()


3. Runs your Tornado app::

   $ env $(cat .env | xargs) python server.py


Works on Projects
-----------------

In development, we can work with per-project environments but no more typing
``source foo/bar``.

I recommend to put your project-specified environment variables in
``{PROJECT_ROOT}/.env`` and mark the ``.env`` as ignored in your VCS. For
example, you can write ``/.env`` in ``.gitignore`` if you are using Git, and
put a ``.env.example`` as a copying template for new-cloned projects.

And then, you can use some utility such as `honcho`_ or `autoenv`_ to apply
the ``.env`` automatically.

For honcho::

    $ echo 'MYPROJECT_DEBUG=true' >> .env
    $ echo 'web: python manage.py runserver' >> Procfile
    $ honcho run python manage.py check-debug
    True
    $ honcho start web
    Starting development server at http://127.0.0.1:5000/
    ...

For autoenv::

    $ echo 'MYPROJECT_DEBUG=true' >> myproject/.env
    $ cd myproject
    $ python manage.py check-debug
    True
    $ python manage.py runserver
    Starting development server at http://127.0.0.1:5000/
    ...


Issues
------

If you want to report bugs or request features, please create issues on
`GitHub Issues <https://github.com/tonyseek/python-envcfg/issues>`_.


.. _12-Factor: http://12factor.net
.. _honcho: https://github.com/nickstenning/honcho
.. _autoenv: https://github.com/kennethreitz/autoenv

.. |Build Status| image:: https://travis-ci.org/tonyseek/python-envcfg.svg?branch=master,develop
   :target: https://travis-ci.org/tonyseek/python-envcfg
   :alt: Build Status
.. |Coverage Status| image:: https://img.shields.io/coveralls/tonyseek/python-envcfg/develop.svg
   :target: https://coveralls.io/r/tonyseek/python-envcfg
   :alt: Coverage Status
.. |Wheel Status| image:: https://img.shields.io/pypi/wheel/python-envcfg.svg
   :target: https://warehouse.python.org/project/python-envcfg
   :alt: Wheel Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/python-envcfg.svg
   :target: https://pypi.python.org/pypi/python-envcfg
   :alt: PyPI Version
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/python-envcfg.svg
   :target: https://pypi.python.org/pypi/python-envcfg
   :alt: Downloads
