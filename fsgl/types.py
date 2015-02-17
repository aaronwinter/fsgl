from enum import Enum


Primitives = Enum('States',
                  ' '.join(['INT', 'STRING', 'BOOL', 'SYMBOL', 'NIL']),
                  module=__name__)


class Type():
    def infer_primitive(thing):
        if thing == 'true' or thing == 'false':
            return Primitives.BOOL
        elif thing == 'nil':
            return Primitives.NIL
        elif thing[0] == '\"' and thing[-1] == '\"':
            return Primitives.STRING
        elif thing[0] == ':':
            return Primitives.SYMBOL


class List(Type):
    def __init__(self, data):
        self.head = data[0]
        self.tail = data[1:]

    def __hash__(self):
        return hash(tuple('LIST', self.data))


class Vector(Type):
    def __init__(self, data=[]):
        self.data = data

    def __hash__(self):
        return hash(tuple('VECTOR', self.data))

    def append(self, *args):
        return Vector(self.data + args)

    def get(self, i):
        return self.data[i]


class Map(Type):
    def __init__(self):
        self.data = {}

    def __call__(self, key):
        return self.data[key]
