import sys
import io
from fsgl.parser import Parser
from fsgl.stdlib import STDLIB

if __name__ == '__main__':
    incode = sys.argv[1] if (len(sys.argv) > 1) else None

    p = Parser(STDLIB)  # initialize parser with stdlib presets
    if incode:
        with open(sys.argv[1], 'r') as f:
            p.eval(f)
    else:
        # repl
        try:
            while True:
                sys.stdout.write('fsgl> ')
                incode = input()
                print(incode)
                p.eval(io.StringIO(incode))
        except (KeyboardInterrupt, EOFError, SystemExit):
            print('\nBye!')
            sys.exit()
