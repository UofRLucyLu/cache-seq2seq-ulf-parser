#!/usr/bin/python3

import subprocess
import cl4py
import sys

if __name__ == "__main__":
    lisp = cl4py.Lisp(quicklisp=True)
    cl = lisp.function('find-package')('CL')
    ql = cl.find_package('QL')
    ql.quickload('ULF-LIB')
    compose_types = lisp.function('ulf-lib::compose-type-string!')
    
    type1 = sys.argv[1]
    type2 = sys.argv[2]
    sys.stdout.write(compose_types(type1, type2))  