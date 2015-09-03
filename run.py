#!/usr/bin/env python

import subprocess
import os
import sys

history = "-h" in sys.argv

try:
    outerhistory = ""
    innerhistory = ""
    while True:
        outer = ""
        inner = ""

        outerbraces = 0
        innerbraces = 0
        lastbrace = None

        c_file = open("main.c", "w")

        c_file.write("#include <stdio.h>\n\n")
        # c_file.write("#include <stdio.h>")

        nextline = raw_input("> ").strip()
        while len(nextline) > 0 and nextline[0] == ">":
            nextline = nextline[1:].strip()
        while nextline != "":
            #if nextline[-1] not in ";{}[(":
            #    nextline += ";"

            if nextline[-1] != ";" and "{" not in nextline and "}" not in nextline:
                nextline = "printf(" + nextline + ");"

            if "{" in nextline:
                if "class" in nextline or "enum" in nextline or "void" in nextline or "public" in nextline or "private" in nextline:
                    outerbraces += 1
                    lastbrace = "outer"
                else:
                    innerbraces += 1
                    lastbrace = "inner"

            if outerbraces > 0:
                outer += nextline
                if history:
                    outerhistory += nextline
            else:
                inner += nextline
                if history:
                    innerhistory += nextline

            if "}" in nextline:
                if lastbrace == "outer":
                    outerbraces -= 1
                else:
                    innerbraces -= 1
            
            nextline = raw_input("> ").strip()
            while len(nextline) > 0 and nextline[0] == ">":
                nextline = nextline[1:].strip()

        c_file.write(outer)
        c_file.write("main() {")
        c_file.write(inner)
        c_file.write("}")

        c_file.close()

        print("\n")

        FNULL = open(os.devnull, "w")

        subprocess.call("cc main.c", stderr = FNULL, shell = True)

        subprocess.call("./a.out", shell = True) 

        print("\n")
except (KeyboardInterrupt, EOFError):
    if "main.c" in os.listdir("."):
        subprocess.call("rm main.c", shell = True)
    if "a.out" in os.listdir("."):
        subprocess.call("rm a.out", shell = True)

    print("")
