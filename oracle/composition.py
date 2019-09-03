from __future__ import print_function
import subprocess
import sys
import os

class Composition():
    def __init__(self, func):
        self.func = func

    def eval(self, args):
        if self.func == 'ulf_type' or self.func == 'compose_types':
            cmd = ['python3', './oracle/{}.py'.format(self.func)]
            if isinstance(args, list):
                cmd.extend(args)
            else:
                cmd.append(args)

            os.environ['PYTHONUNBUFFERED'] = '1'
            PY3 = subprocess.Popen(cmd,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                universal_newlines = True)

        else:
            print('Wrong function!')
            return None

        output = []
        while PY3.poll() is None:
            line = PY3.stdout.readline()
            #print(line)
            if line != "":
                output.append(line)
                #print(line, end='')
        
        results = []
        size = len(args)
        for i in range(1, size + 1):
            results.append(output[-(size + 1 - i)].strip())
        return results

if __name__ == "__main__":
    ulf_type = Composition('ulf_type')
    type1 = ulf_type.eval(['(dog.n)', '(bark.v)'])
    """
    type2 = ulf_type.eval('(cat.n)')
    compose_types = Composition('compose_types')
    print('***res='+compose_types.eval([type1, type2]))
    """