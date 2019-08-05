#!/usr/bin/python3

import subprocess
import cl4py
import sys

if __name__ == "__main__":
    lisp = cl4py.Lisp(quicklisp=True)
    cl = lisp.function('find-package')('CL')
    ql = cl.find_package('QL')
    ql.quickload('ULF-LIB')
    ulf_type = lisp.function('ulf-lib::str-ulf-type-string?')
    
    atom = sys.argv[1]
    sys.stdout.write(ulf_type(atom)+'\n')