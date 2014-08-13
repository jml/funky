import contextlib
import functools


def get_globals(function):
    return list(function.func_code.co_names)


def call_with_globals(global_overrides, function, *args, **kwargs):
    with mutated_dict(function.func_globals, global_overrides):
        return function(*args, **kwargs)


@contextlib.contextmanager
def mutated_dict(original, updates):
    backup = dict(original)
    original.update(updates)
    yield
    original.update(backup)
    for key in updates.viewkeys() - backup.viewkeys():
        del original[key]


_OVERRIDE_PREFIX = '_override_'
_OVERRIDE_PREFIX_LEN = len(_OVERRIDE_PREFIX)

def funkify(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        new_globals = {}
        for name in kwargs.keys():
            if name.startswith(_OVERRIDE_PREFIX):
                new_globals[name[_OVERRIDE_PREFIX_LEN:]] = kwargs.pop(name)
        return call_with_globals(new_globals, function, *args, **kwargs)
    return wrapper


class ImpureFunction(Exception):
    pass


def pure(function):
    if get_globals(function):
        raise ImpureFunction(function)
    return function
