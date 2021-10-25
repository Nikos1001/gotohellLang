
import tokenizer
import parser
import sys

file = open('guess.esolang')
source = file.read()

tokenizer.init(source)

code = parser.parse()
if parser.had_error:
    quit(-1)

class Floppy:

    size = 0
    data = []
    cell = 0

    def __init__(self, size):
        self.size = size
        self.data = [0] * size

line = code['min_line']
cont = True
vars = {}
input_queue = ''

floppies = {}
floppy = None
spinning = False

def eval_expr(expr):
    if expr['type'] == 'literal':
        return expr['value']
    elif expr['type'] == 'var':
        return vars[expr['value']]
    elif expr['type'] == 'binary':
        a = eval_expr(expr['a'])
        b = eval_expr(expr['b'])
        if expr['op'] == '+':
            return a + b
        if expr['op'] == '-':
            return a - b
        if expr['op'] == '*':
            return a * b
        if expr['op'] == '/':
            return a // b

prev_line = line
while cont:
    if not line in code:
        print('fatal runtime error. line ' + str(line) + ' doesn\'t exsist.', file=sys.stderr)
        print('previous line ' + str(prev_line) + '.', file=sys.stderr)
        break
    prev_line = line
    for stmt in code[line]:
        if stmt['type'] == 'print':
            print(chr(eval_expr(stmt['value'])), end='')
        if stmt['type'] == 'get':
            while len(input_queue) == 0:
                input_queue = input()
            vars[stmt['varname']] = ord(input_queue[0])
            input_queue = input_queue[1:]
        if stmt['type'] == 'goto':
            line = eval_expr(stmt['line'])
        if stmt['type'] == 'varset':
            vars[stmt['varname']] = eval_expr(stmt['value'])
        if stmt['type'] == 'floppy':
            floppies[stmt['name']] = Floppy(stmt['size'])
        if stmt['type'] == 'insert':
            if spinning:
                print('cannot insert disk while spinning.', file=sys.stderr)
            else:
                floppy = floppies[stmt['name']]
        if stmt['type'] == 'write':
            if floppy == None:
                print('cannot write to non-exsistant disk.', file=sys.stderr)
            else:
                floppy.data[floppy.cell] = eval_expr(stmt['value'])
        if stmt['type'] == 'read':
            if floppy == None:
                print('cannot read from non-exsistant disk.', file=sys.stderr)
            else:
                vars[stmt['name']] = floppy.data[floppy.cell]
        if stmt['type'] == 'spin':
            spinning = True
        if stmt['type'] == 'stop':
            spinning = False
        if stmt['type'] == 'end':
            cont = False
        
    if spinning and floppy != None:
        floppy.cell += 1
        if floppy.cell >= floppy.size:
            floppy.cell = 0