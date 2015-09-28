# C Playground
A quick way to run bits of C code, made with Python

This script is made especially useful by this line in my .bashrc: 
alias cpg="python /Users/npward/Dropbox/Random/C\ Playground/run.py"

Now, by typing "cpg" into the Terminal, I am immediately given a C prompt. This works, in theory, like the Python interpreter: I can type bits of C code, whether one line or multiple, and see the results. It also cleans up the output a bit when there are errors (and adds red text!).

Of course, there are many problems and bugs, which I haven't yet fixed (and probably won't get around to).  This project is based on my earlier "Java Playground", but because C is annoying, there are more problems here (for instance, in Java Playground typing "4+9" will correctly print "13", because the Playground sees the semicolon-less line and prints the result; the C playground attempts to do the same, but because printf can only print strings, no output is produced).

