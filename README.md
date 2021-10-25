
# GotoHell

GotoHell(as in Goto Hell, not Go To Hell) is an esoteric programming language based on BASIC.

Lines of code in GotoHell consist of their line number, followed by a `|`, followed by a series of statements separated by colons.
Execution starts on the line with the smallest number. Note that after a line is done executing, it does not automatically go to the next line.

GotoHell has the following commands:
```
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
```

Conditional logic is done by `goto`ing to different lines based on a variable. For instance, this code:
```
10 | goto 20 + 10 * x
20 | print 65 : end
30 | print 66 : end
```
will print `A` if x = 0, and `B` if x = 1.

In GotoHell, data storage is done using floppy disks. You declare a floppy using the `floppy` command. After `insert`ing the floppy, you can read/write to the read head. If you want to move said read head, use the `spin` command. After the disk starts spinning, it will shift the read head by one cell every line that gets executed(if it goes beyond the last cell, it loops back to the first). You can stop the disk with `stop`. There is no way to tell where you are on the disk. There is no way to reverse the disk.