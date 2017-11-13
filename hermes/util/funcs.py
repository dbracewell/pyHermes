import functools


def get_if_none(arg, default):
    return arg if arg else default


def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose2, functions, lambda x: x)
