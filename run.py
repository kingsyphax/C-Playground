#!/usr/bin/env python

import subprocess
import os
import sys
import string

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
                inner += nextline + "\n"
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
        c_file.write("main() {\n")
        c_file.write(inner)
        c_file.write("\n}")

        c_file.close()

        print("")

        err_output = open("err_output.txt", "w")
        subprocess.call("cc main.c", stderr = err_output, shell = True)
        err_output.close()

        err_input = open("err_output.txt", "r")
        err_lines = err_input.readlines()
        err_input.close()

        if "error generated" in err_lines[-1] or "errors generated" in err_lines[-1]:
            errors_text = err_lines[-1][:err_lines[-1].find("error")-1][::-1]
            errors = ""
            while errors_text[0] in string.digits:
                errors += errors_text[0]
                errors_text = errors_text[1:]
            errors = int(errors[::-1])
        else:
            errors = 0

        if errors > 0:
            print("\033[1m\033[31m%d ERROR%s!\n\033[0m" % (errors, "S" if errors > 1 else ""))
            actual_error_lines = []
            for i in range(len(err_lines) - 1):
                if "error" in err_lines[i]:
                    actual_error_lines.append("\033[1m" + err_lines[i][err_lines[i].find("error")+7:-1] + "\033[0m ")
                    for j in range(i + 1, i + 3):
                        actual_error_lines.append(err_lines[j])
                    i += 3

            for line in actual_error_lines:
                print(line[:-1])
        else:
            subprocess.call("./a.out", shell = True) 

        print("")
except (KeyboardInterrupt, EOFError):
    if "main.c" in os.listdir("."):
        subprocess.call("rm main.c", shell = True)
    if "a.out" in os.listdir("."):
        subprocess.call("rm a.out", shell = True)
    if "err_output.txt" in os.listdir("."):
        subprocess.call("rm err_output.txt", shell = True)

    print("")
