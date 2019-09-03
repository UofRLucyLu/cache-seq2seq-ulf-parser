#!/usr/bin/python3

import subprocess
import cl4py
import sys

# draft method for parsing all types.
# TODO: potential issue with command parsing part. Test that out.
def all_ulf_type(tokens):
    # setting up all the functions rquired
    lisp = cl4py.Lisp(quicklisp=True)
    cl = lisp.function('find-package')('CL')
    ql = cl.find_package('QL')
    ql.quickload('ULF-LIB')
    ulf_type = lisp.function('ulf-lib::str-ulf-type-string?')

    # loop over all tokens in the sentence
    for token in tokens:
        sys.stdout.write(ulf_type(token) + '\n')

if __name__ == "__main__":
    """
    lisp = cl4py.Lisp(quicklisp=True)
    cl = lisp.function('find-package')('CL')
    ql = cl.find_package('QL')
    ql.quickload('ULF-LIB')
    ulf_type = lisp.function('ulf-lib::str-ulf-type-string?')
    
    atom = sys.argv[1]
    sys.stdout.write(ulf_type(atom)+'\n')
    """
    tokens = sys.argv[1:]
    all_ulf_type(tokens)