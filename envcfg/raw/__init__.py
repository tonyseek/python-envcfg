from __future__ import absolute_import

from .._hook import import_hook


@import_hook(__name__)
def value_processor(name, raw_name, raw_value):
    return raw_value


del import_hook
del value_processor
