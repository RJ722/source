# Source : https://stackoverflow.com/a/33876795

st='''import things\nclass foo:\n    #There are comments\n    print "hello" \n\ndef bla():\n    a = 1\n    b = 2\n    c= a+b\n    print c'''

import ast

tree = ast.parse(st)
for entry in tree.body:
    if isinstance(entry, ast.FunctionDef):
        lastBody = entry.body[-1]
        while isinstance (lastBody,(ast.For,ast.While,ast.If)):
            lastBody = lastBody.Body[-1]
        lastLine = lastBody.lineno
        print "Name: ",entry.name
        print "First Line: ",entry.lineno
        print "LastLine: ",lastLine
        print "Source: "
        if isinstance(st,str):
            st = st.split("\n")
        for i , line in enumerate(st,1):
            if i in range(entry.lineno,lastLine+1):
                print line

    if isinstance(entry, ast.ClassDef):
        lastBody = entry.body[-1]
        while isinstance (lastBody,(ast.For,ast.While,ast.If)):
            lastBody = lastBody.Body[-1]
        lastLine = lastBody.lineno
        print "Name: ",entry.name
        print "First Line: ",entry.lineno
        print "Last Line: ",lastLine
        print "Source: "
        if isinstance(st,str):
            st = st.split("\n")
        for i , line in enumerate(st,1):
            if i in range(entry.lineno,lastLine+1):
                print line
