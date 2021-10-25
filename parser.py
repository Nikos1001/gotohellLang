
import tokenizer
import sys

panic = False
had_error = False
line_number = -1

def error(message):
    global panic, had_error
    had_error = True
    if panic:
        return
    panic = True
    print('line ' + str(line_number), file=sys.stderr)
    print(message, file=sys.stderr)

def parse_literal():
    if tokenizer.current.type == 'num':
        val = tokenizer.current.value
        tokenizer.advance()
        return {
            'type': 'literal',
            'value': val
        }
    if tokenizer.current.type == 'name':
        varname = tokenizer.current.value
        tokenizer.advance()
        return {
            'type': 'var',
            'value': varname
        }
    if tokenizer.current.type == '(':
        tokenizer.advance()
        expr = parse_expr()
        tokenizer.advance()
        return expr
    error('expected expression')
    tokenizer.advance()

def parse_multiplicative():
    a = parse_literal()
    while tokenizer.current.type == '*' or tokenizer.current.type == '/':
        op = tokenizer.current.type
        tokenizer.advance()
        b = parse_literal()
        a = {
            'type': 'binary',
            'a': a,
            'b': b,
            'op': op
        }
    return a

def parse_additive():
    a = parse_multiplicative()
    while tokenizer.current.type == '+' or tokenizer.current.type == '-':
        op = tokenizer.current.type
        tokenizer.advance()
        b = parse_multiplicative()
        a = {
            'type': 'binary',
            'a': a,
            'b': b,
            'op': op
        }
    return a

def parse_expr():
    return parse_additive()

def parse_stmt():
    if tokenizer.current.type == 'print':
        tokenizer.advance()
        return {
            'type': 'print',
            'value': parse_expr()
        }
    if tokenizer.current.type == 'get':
        tokenizer.advance()
        if tokenizer.current.type != 'name':
            error('expected variable name.')
        varname = tokenizer.current.value
        tokenizer.advance()
        return {
            'type': 'get',
            'varname': varname
        }
    elif tokenizer.current.type == 'goto':
        tokenizer.advance()
        return {
            'type': 'goto',
            'line': parse_expr()
        }
    elif tokenizer.current.type == 'name':
        varname = tokenizer.current.value
        tokenizer.advance()
        if tokenizer.current.type != '=':
            error('expected =.')
        tokenizer.advance()
        return {
            'type': 'varset',
            'varname': varname,
            'value': parse_expr()
        }
    elif tokenizer.current.type == 'floppy':
        tokenizer.advance()
        if tokenizer.current.type != 'name':
            error('expected floppy disk name.')
        name = tokenizer.current.value
        tokenizer.advance()
        if tokenizer.current.type != 'num':
            error('expected floppy disk size.')
        size = tokenizer.current.value
        tokenizer.advance()
        return {
            'type': 'floppy',
            'name': name,
            'size': size
        }
    elif tokenizer.current.type == 'insert':
        tokenizer.advance()
        if tokenizer.current.type != 'name':
            error('expected floppy disk name.')
        name = tokenizer.current.value
        tokenizer.advance()
        return {
            'type': 'insert',
            'name': name
        }
    elif tokenizer.current.type == 'spin':
        tokenizer.advance()
        return {
            'type': 'spin'
        }
    elif tokenizer.current.type == 'stop':
        tokenizer.advance()
        return {
            'type': 'stop'
        }
    elif tokenizer.current.type == 'write':
        tokenizer.advance()
        return {
            'type': 'write',
            'value': parse_expr()
        }
    elif tokenizer.current.type == 'read':
        tokenizer.advance()
        if tokenizer.current.type != 'name':
            error('expected variable name.')
        name = tokenizer.current.value
        tokenizer.advance()
        return {
            'type': 'read',
            'name': name
        }
    elif tokenizer.current.type == 'end':
        tokenizer.advance()
        return {
            'type': 'end'
        }

    error('expected statement.')
    return None

def parse_line():
    global panic, line_number
    while tokenizer.current.type == '\n':
        tokenizer.advance()
    
    line_number = tokenizer.current.value
    if tokenizer.current.type != 'num':
        line_number = -1
        error('expected line number.')
    tokenizer.advance()
    if tokenizer.current.type != '|':
        error('expected |.')
    tokenizer.advance()

    stmts = []
    while tokenizer.current.type != '\n' and tokenizer.current.type != 'eof':
        stmts.append(parse_stmt())
        if tokenizer.current.type == ':':
            tokenizer.advance()
            if tokenizer.current.type == '\n':
                error('expected statment.')
        elif tokenizer.current.type != '\n' and tokenizer.current.type != 'eof':
            error('expected newline.')
            tokenizer.advance()

    panic = False

    return {
        'line': line_number,
        'stmts': stmts
    }

def parse():
    code = {}
    min_line = 1000000000
    while tokenizer.current.type != 'eof':
        line = parse_line()
        code[line['line']] = line['stmts']
        min_line = min(min_line, line['line'])
    code['min_line'] = min_line
    return code