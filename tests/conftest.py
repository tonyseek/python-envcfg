import os

from pytest import fixture


@fixture(scope='function')
def environ(request):
    origin = dict(os.environ)

    @request.addfinalizer
    def restore_environ():
        os.environ.clear()
        os.environ.update(origin)

    return os.environ
