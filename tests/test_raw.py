from pytest import raises


def test_success(environ):
    environ['ENVCFG_RAW_1_BOOLEAN'] = 'true'
    environ['ENVCFG_RAW_1_INTEGER'] = '42'
    environ['ENVCFG_RAW_1_REAL'] = '42.42'
    environ['ENVCFG_RAW_1_STRING'] = '"42"'
    environ['ENVCFG_RAW_1_DICT'] = '{"value": 42}'

    from envcfg.raw.envcfg_raw_1 import (
        BOOLEAN,
        INTEGER,
        REAL,
        STRING,
        DICT,
    )
    assert BOOLEAN == 'true'
    assert INTEGER == '42'
    assert REAL == '42.42'
    assert STRING == '"42"'
    assert DICT == '{"value": 42}'


def test_failed():
    with raises(ImportError) as einfo:
        import envcfg.raw._private_module  # noqa
    assert einfo.value.args[0].startswith(
        'No module named envcfg.raw._private_module')

    with raises(ImportError) as einfo:
        import envcfg.raw.INVALID_NAME  # noqa
    assert einfo.value.args[0].startswith(
        'No module named envcfg.raw.INVALID_NAME')
