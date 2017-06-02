# Source : https://stackoverflow.com/a/33876795

from __future__ import print_function

import ast

source = '''\
import things
class foo1:
    #There are comments
    print("hello")

class foo2:
    if False:
        pass

class foo3:
    with open('test') as f:
        pass

# This test case fails.
class foo4:
    try:
        foo()
    except:
        pass

class foo5:
    def bar():
        pass

class foo6:
    class test:
        pass

# This test case fails.
class foo7:
    if True:
        print(1)
    else:
        print(0)
'''

# TODO: Add tests and probably code for
# AsyncFunctionDef, AsyncWith, AsyncFor

tree = ast.parse(source)
for entry in tree.body:
    if isinstance(entry, (ast.ClassDef, ast.FunctionDef)):
        print('Body', entry.body)
        last_body = entry.body[-1]
        while isinstance(last_body, (ast.ClassDef, ast.For, ast.FunctionDef, ast.If, ast.While, ast.With)):
            print('Available fields:', dir(last_body))
            print('Body', last_body.body)
            # TODO: For some ast node types this is too simple. For
            # example for try-except, we will have to
            # check for ast.Try.finalbody, ast.Try.orelse and
            # ast.Try.handlers sequentially and move to the first defined
            # attribute among these.
            # Similarly for if-else. For Python 2 there is no ast.Try,
            # but only ast.TryExcept and ast.TryFinally. The code here
            # only works for ast nodes that only have one child "body".
            last_body = last_body.body[-1]

        last_line = last_body.lineno
        print("Name: ", entry.name)
        print("First line: ", entry.lineno)
        print("Last line: ", last_line)
        print("Source: ",)
        if isinstance(source, str):
            source = source.split("\n")
        for i, line in enumerate(source, 1):
            if i in range(entry.lineno, last_line + 1):
                print(line)
