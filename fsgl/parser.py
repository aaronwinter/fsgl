from enum import Enum
from .syntax_tree import SyntaxTree
from .types import List, Vector, Map

DEBUG = True

States = Enum('States',
              ' '.join(['READ', 'COMMENT', 'TOKEN', 'SETVAR', 'FUNCTION',
              'FUNCCALL', 'INTEGER', 'STRING', 'SYMBOL', 'LIST', 'VECTOR',
              'MAP']),
              module=__name__)


# parse entire code as a single body,
class Parser():
    def __init__(self, environ={}, repl=False):
        self.environ = environ
        self.repl = repl
        self.state = States.READ
        self.lexeme = ''

        # managing computations on a stack
        self.varname = ''
        self.var = ''
        self.var_stack = []

        # managing function calls
        self.func = None
        self.call_stack = []

        # for easy prev state transition
        self.state_stack = []

    def goto_state(self, state):
        self.state_stack.append(self.state)
        self.state = state

    def goto_typed_state(self, c):
        '''
        Push the current state on to the stack and transition to a state that
        is "typed" (i.e. reading in a typed value)
        '''
        self.var = c

        if c.isdigit():
            self.goto_state(States.INTEGER)
        elif c.isalpha():
            self.goto_state(States.TOKEN)
        elif c == '(':
            self.goto_state(States.LIST)
        elif c == '[':
            self.goto_state(States.VECTOR)
        elif c == '#':
            self.goto_state(States.MAP)
        elif c == '\"':
            self.goto_state(States.STRING)

    def goto_prev_state(self):
        self.state = self.state_stack.pop()

    def emit(self, value, print_output=False):
        '''
        Emit a value to output.
        If print_output or self.repl is True, print it.
        '''
        if print_output or self.repl:
            print(value)

    def eval(self, code):
        '''
        The basic DFA parsing code.
        '''
        readable = True
        nextchar = code.read(1)
        while readable:
            c = nextchar
            nextchar = code.read(1)
            if c == '':  # EOF
                code.close()
                readable = False
            if not c.isspace():
                self.lexeme += c

            if DEBUG:
                print('read char:', c)
                print('next char:', nextchar)
                print('state:', self.state)

            # parse by character
            if self.state == States.READ:
                if c == '=':
                    self.goto_state(States.SETVAR)
                elif c == ';':
                    self.goto_state(States.COMMENT)
                else:
                    self.goto_typed_state(c)

            elif self.state == States.COMMENT:
                if c == '\n':  # keep ignoring until newline
                    self.goto_prev_state()

            elif self.state == States.TOKEN:
                if c == '(':
                    self.goto_state(States.FUNCCALL)
                else:
                    if not nextchar.isalpha():
                        # check for reserved tokens
                        if self.lexeme == 'true':
                            self.var = True
                        elif self.lexeme == 'false':
                            self.var = False
                        elif self.lexeme == 'nil':
                            self.var = None
                        else:
                            self.varname = self.lexeme
                            if self.varname in self.environ:
                                self.var = self.environ[self.varname]
                            else:
                                self.var = ''

                        self.lexeme = ''
                        self.goto_prev_state()

            elif self.state == States.SETVAR:
                if self.var:
                    if self.varname in self.environ:
                        raise 'Cannot mutate value %s' % (self.varname)
                    else:
                        if DEBUG:
                            print('setting %s to %s', self.varname, self.var)
                        self.environ[self.varname] = self.var
                        self.var = ''
                        self.goto_prev_state()
                if c == '>':  # =>
                    self.goto_state(States.FUNCTION)
                elif not c.isspace():
                    self.lexeme = ''
                    self.goto_typed_state(nextchar)

            elif self.state == States.FUNCTION:
                if c == '{':
                    pass
                elif c == '}':
                    self.goto_prev_state()
                else:
                    # function body parse
                    pass

            elif self.state == States.FUNCCALL:
                # this is a function call, read arg list
                if not self.func:
                    func = self.environ[self.lexeme]
                    if callable(func):
                        self.func = func
                    else:
                        raise 'not a function'

            elif self.state == States.INTEGER:
                if c.isdigit():
                    self.var += c
                if not nextchar.isdigit():
                    self.var = int(self.var)
                    self.goto_prev_state()

            elif self.state == States.STRING:
                # todo: placeholders
                if c == '\\':
                    # escaped characters is a "sub-state" that returns to prev
                    # state after reading 1 character
                    nextc = c.read(1)
                    if nextc == 'n':
                        self.var += '\n'
                    else:
                        self.var += nextc
                elif c == '\"':
                    self.goto_prev_state()
                else:
                    self.var += c

            elif self.state == States.SYMBOL:
                if c.isalpha() or c.isdigit():
                    # append any a-zA-Z0-9 to the symbol
                    self.var += c
                else:
                    self.goto_prev_state()

            elif self.state == States.LIST:
                # list literal syntax: (a, b, c, ...)
                if c == ',':
                    # append current item onto list being built
                    item = self.var
                    self.var = self.var_stack.pop()
                    self.var.append(item)
                    self.var_stack.append(self.var)
                    self.goto_typed_state(c)
                elif c == ')':
                    self.var = List(self.var)
                    self.goto_prev_state()

            elif self.state == States.VECTOR:
                # vector syntax: [a, b, c, ...]
                if c == ',':
                    item = self.var
                    self.var = self.var_stack.pop()
                    self.var.append(item)
                    self.var_stack.append(self.var)
                    self.goto_typed_state(c)
                elif c == ']':
                    self.var = Vector(self.var)
                    self.goto_prev_state()

            elif self.state == States.MAP:
                # map syntax: {k v, k v, ...}
                if c == ',':
                    k, v = tuple(self.var)
                    self.var_stack[-1].append((k, v))
                    self.var = []
                elif c.isspace():
                    if len(self.var) < 2:
                        self.var.append(self.var)
                elif c == '{':
                    pass
                elif c == '}':
                    self.var = Map(self.var)
                    self.goto_prev_state()

            if DEBUG:
                print('next state:', self.state)
                print('state_stack:', self.state_stack)
                print('environ:', self.environ)
                print('lexeme:', self.lexeme)
                print('varname:', self.varname)
                print('var:', self.var)
                print()
        else:
            # when finished parsing, emit computed value
            self.emit(self.var)
            self.state_stack = []
            self.state = States.READ
