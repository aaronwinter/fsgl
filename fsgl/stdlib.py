import operator
from .types import List, Vector, Map

def _prints(s):
    print(s)


def _mult(*args):
    res = 1
    for a in args:
        res *= a
    return res


def _and(*args):
    for a in args:
        if not a:
            return False
    return True


def _or(*args):
    for a in args:
        if a:
            return True


def _div(*args):
    res = args[0]
    for a in args[1:]:
        res /= a
    return res


STDLIB = {
    'prints': _prints,
    'gets': None,
    '+': sum,
    '-': (lambda *args: args[0] - sum(args[1:])),
    '*': _mult,
    '/': _div,
    'if': (lambda exp, a, b: a if exp else b),
    'equals': (lambda a, b: a == b),
    'and': _and,
    'or': _or,
    'not': (lambda a: not a),
    'cons': (lambda h, t: List(h, t)),
    'head': (lambda l: l.head),
    'tail': (lambda l: l.tail),
}
