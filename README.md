
# GotoHell

This is an esoteric programming language based on BASIC.

Lines of code in GotoHell consist of their line number, followed by a `|`, followed by a series of statements separated by colons.
Execution starts on the line with the smallest number. Note that after a line is done executing, it does not automatically go to the next line.

GotoHell has the following commands:
``
print <expression> -> prints the value of the expression as an ASCII character
get <varname> -> gets a character of user input, and saves it's ASCII code to the given varname 
goto <expression> -> goes to the line numbered with the value of the expression
end -> terminates the program
floppy <name> <size> -> declares a new floppy disk with a given name and size(size must be a constant number)
insert <name> -> inserts the floppy disk with the given name into the floppy drive
spin -> begins spinning the disk
stop -> stops spinning the disk
read <varname> -> reads the value at the floppy disk read head to a variable
write <expression> -> writes the value of the expression to the floppy disk read head
``