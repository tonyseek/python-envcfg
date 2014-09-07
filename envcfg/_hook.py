import os
import re
import sys
import types


class ImportHook(object):

    re_module_name = re.compile(r'[a-z][a-z0-9_]*')

    def __init__(self, wrapper_module, value_processor):
        self.wrapper_module = wrapper_module
        self.wrapper_prefix = wrapper_module + '.'
        self.value_processor = value_processor

    def __eq__(self, other):
        return self.__class__.__module__ == other.__class__.__module__ and \
            self.__class__.__name__ == other.__class__.__name__ and \
            self.wrapper_module == other.wrapper_module

    def __ne__(self, other):
        return not self.__eq__(other)

    def install(self):
        sys.meta_path[:] = [x for x in sys.meta_path if self != x] + [self]

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.wrapper_prefix):
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        prefix_name = fullname[len(self.wrapper_prefix):]
        if not self.re_module_name.match(prefix_name):
            error_msg = ('No module named {0}\n\nThe name of envvar module '
                         'should matched {1.pattern}')
            raise ImportError(error_msg.format(fullname, self.re_module_name))

        module = types.ModuleType(fullname)
        for name, value in self.load_environ(prefix_name):
            setattr(module, name, value)
        sys.modules[fullname] = module

        return module

    def load_environ(self, prefix_name):
        prefix = prefix_name.upper() + '_'
        for raw_name, raw_value in os.environ.items():
            if not raw_name.startswith(prefix):
                continue
            if raw_name == prefix:
                continue
            name = raw_name[len(prefix):]
            value = self.value_processor(name, raw_name, raw_value)
            yield name, value


def import_hook(wrapper_module):
    def wrapper(fn):
        hook = ImportHook(wrapper_module, value_processor=fn)
        hook.install()
    return wrapper
