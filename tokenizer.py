
src = ''
curr_idx = 0

class Token:
    
    type = 'number'
    value = None

    def __init__(self, type, value):
        self.type = type 
        self.value = value

current = None

whitespace = [' ', '\t']
single_chars = ['\n', '|', ':', '+', '-', '*', '/', '=', '(', ')']
keywords = ['get', 'print', 'goto', 'end', 'floppy', 'insert', 'spin', 'write', 'read', 'stop']
def advance():
    global curr_idx, current

    if curr_idx >= len(src):
        current = Token('eof', None)
        return
    
    while src[curr_idx] in whitespace and curr_idx < len(src):
        curr_idx += 1

    if curr_idx >= len(src):
        current = Token('eof', None)
        return
    
    if src[curr_idx] in single_chars:
        current = Token(src[curr_idx], None)
        curr_idx += 1
        return
    if src[curr_idx].isdigit():
        val = ''
        while curr_idx < len(src) and src[curr_idx].isdigit():
            val += src[curr_idx]
            curr_idx += 1
        current = Token('num', int(val))
        return
    if src[curr_idx].isalpha():
        val = ''
        while curr_idx < len(src) and src[curr_idx].isalpha():
            val += src[curr_idx]
            curr_idx = curr_idx + 1
        if val in keywords:
            current = Token(val, None)
        else:
            current = Token('name', val)
        return
    
    current = Token('error', None)
    curr_idx = curr_idx + 1
    
def init(source):
    global src, curr_idx
    src = source
    curr_idx = 0
    advance()