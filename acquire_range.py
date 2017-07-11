# Source : https://stackoverflow.com/a/33876795

from __future__ import print_function

import ast
import sys


TRAVERSABLE_FIELDS = {
        ast.ClassDef: ('decorator_list', 'body', ),
        ast.ExceptHandler: ('body',),
        ast.For: ('body', 'orelse'),
        ast.FunctionDef: ('decorator_list', 'body',),
        ast.If: ('body', 'orelse'),
        ast.Module: ('body',),
        ast.While: ('body', 'orelse'),
        ast.With: ('body',),
}
if sys.version_info < (3, 0):
    TRAVERSABLE_FIELDS.update({
        ast.TryExcept: ('body', 'handlers', 'orelse'),
        ast.TryFinally: ('body', 'finalbody'),
    })
else:
    TRAVERSABLE_FIELDS.update({
        ast.Try: ('body', 'handlers', 'orelse', 'finalbody')
    })

ENTRY_POINTS = (ast.ClassDef, ast.FunctionDef)


source = '''\
# All test cases pass
import things

class Foo:
    #There are comments
    print("hello")

class Foo:
    if False:
        pass

class Foo:
    with open('test') as f:
        pass

class Foo:
    try:
        foo()
    except:
        pass
    else:
        foobar()

class Foo:
    def bar():
        pass

class Foo:
    class test:
        pass

class Foo:
    if True:
        print(1)
    else:
        print(0)

class Foo:
    def __init__(self):
        pass

    @prop
    def _func_bar():
        pass

class Foo:
    try:
        foo()
    except:
        bar()

class Foo:
    for x in [1]:
        print(x)
    else:
        print("Foo")

class Foo:
    x = [1]
    while x:
        x.pop
    else:
        print("Foo")
'''

# TODO: Add tests and probably code for
# AsyncFunctionDef, AsyncWith, AsyncFor

tree = ast.parse(source)
for entry in tree.body:
    if isinstance(entry, ENTRY_POINTS):
        print('Body', entry.body)
        last_body = entry.body[-1]
        while isinstance(last_body, tuple(TRAVERSABLE_FIELDS.keys())):
            fields = TRAVERSABLE_FIELDS[last_body.__class__]
            print('Available fields:', fields)
            print('Body', last_body.body)
            for field in reversed(fields):
                children = getattr(last_body, field)
                if children:
                    break
            print("Children:", children)
            last_body = children[-1] # The last child

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
