from pytest import raises


def test_success(environ):
    environ['SUCHDOGE_BOOLEAN'] = 'true'
    environ['SUCHDOGE_INTEGER'] = '42'
    environ['SUCHDOGE_REAL'] = '42.42'
    environ['SUCHDOGE_STRING'] = '"42"'
    environ['SUCHDOGE_DICT'] = '{"value": 42}'
    environ['SUCHDOGE_RAW_STR'] = 'foo'

    from envcfg.smart.suchdoge import (
        BOOLEAN,
        INTEGER,
        REAL,
        STRING,
        DICT,
        RAW_STR,
    )
    assert BOOLEAN is True
    assert INTEGER == 42
    assert REAL == 42.42
    assert STRING == '42'
    assert DICT == {'value': 42}
    assert RAW_STR == 'foo'


def test_failed(environ):
    with raises(ImportError) as einfo:
        import envcfg.smart._private_module  # noqa
    assert einfo.value.args[0].startswith(
        'No module named envcfg.smart._private_module')

    with raises(ImportError) as einfo:
        import envcfg.smart.INVALID_NAME  # noqa
    assert einfo.value.args[0].startswith(
        'No module named envcfg.smart.INVALID_NAME')
