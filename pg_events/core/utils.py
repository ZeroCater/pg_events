import importlib
import sys
import os
from contextlib import contextmanager
import imp as _imp


class NotAPackage(Exception):
    pass


@contextmanager
def cwd_in_path():
    """Context adding the current working directory to sys.path."""
    cwd = os.getcwd()
    if cwd in sys.path:
        yield
    else:
        sys.path.insert(0, cwd)
        try:
            yield cwd
        finally:
            try:
                sys.path.remove(cwd)
            except ValueError:  # pragma: no cover
                pass


def find_module(module, path=None, imp=None):
    """supporting dots"""
    if imp is None:
        imp = importlib.import_module
    with cwd_in_path():
        if '.' in module:
            last = None
            parts = module.split('.')
            for i, part in enumerate(parts[:-1]):
                mpart = imp('.'.join(parts[:i + 1]))
                try:
                    path = mpart.__path__
                except AttributeError:
                    raise NotAPackage(module)
                last = _imp.find_module(parts[i + 1], path)
            return last
        return _imp.find_module(module)


def load_module(module):
    res = None
    fp, pathname, description = find_module(module)
    try:
        res = _imp.load_module(module, fp, pathname, description)
    finally:
        if fp:
            fp.close()

    return res
