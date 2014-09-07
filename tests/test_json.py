from pytest import raises


def test_success(environ):
    environ['ENVCFG_JSON_1_BOOLEAN'] = 'true'
    environ['ENVCFG_JSON_1_INTEGER'] = '42'
    environ['ENVCFG_JSON_1_REAL'] = '42.42'
    environ['ENVCFG_JSON_1_STRING'] = '"42"'
    environ['ENVCFG_JSON_1_DICT'] = '{"value": 42}'

    from envcfg.json.envcfg_json_1 import (
        BOOLEAN,
        INTEGER,
        REAL,
        STRING,
        DICT,
    )
    assert BOOLEAN is True
    assert INTEGER == 42
    assert REAL == 42.42
    assert STRING == '42'
    assert DICT == {'value': 42}


def test_failed(environ):
    environ['ENVCFG_JSON_2_INVALID'] = 'foo'

    with raises(ImportError) as einfo:
        import envcfg.json._private_module  # noqa
    assert einfo.value.args[0].startswith(
        'No module named envcfg.json._private_module')

    with raises(ImportError) as einfo:
        import envcfg.json.INVALID_NAME  # noqa
    assert einfo.value.args[0].startswith(
        'No module named envcfg.json.INVALID_NAME')

    with raises(ImportError) as einfo:
        import envcfg.json.envcfg_json_2  # noqa
    assert 'is not a valid json value' in einfo.value.args[0]
