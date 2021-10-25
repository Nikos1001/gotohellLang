#! python3

import sys

string = ' '.join(sys.argv[1:])

result = ''
for char in string:
    result += 'print ' + str(ord(char)) + ' : '
print(result)