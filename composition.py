#!/usr/bin/python

from __future__ import print_function
import subprocess

class Composition():
    def __init__(self, func):
        self.func = func

    def eval(self, args):
        if self.func == 'ulf_type':
            atom = args[0]
            PY3 = subprocess.Popen(['python3', 'ulf_type.py', atom],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                bufsize = 1,
                                universal_newlines = True)
        elif self.func == 'compose_types':
            type1 = args[0]
            type2 = args[1]
            PY3 = subprocess.Popen(['python3', 'compose_types.py', type1, type2],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                bufsize = 1,
                                universal_newlines = True)
        else:
            print('Wrong function!')
            return None

        output, error = PY3.communicate()
        return output

if __name__ == "__main__":
    ulf_type = Composition('ulf_type')
    print(ulf_type.eval('the.d'))