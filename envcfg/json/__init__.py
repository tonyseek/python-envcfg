from __future__ import absolute_import

from .._hook import import_hook


@import_hook(__name__)
def value_processor(name, raw_name, raw_value):
    import json
    try:
        value = json.loads(raw_value)
    except ValueError:
        error_msg = (
            '{0}={1!r} found but {1!r} is not a valid json value.\n\n'
            'You may want {0}=\'"{1}"\' if the value should be a string.')
        raise ImportError(error_msg.format(raw_name, raw_value))
    return value


del import_hook
del value_processor
