from __future__ import print_function

import ast
import sys
from vulture import lines
from vulture.core import ENCODING_REGEX


def annotate(source, tree):
    for entry in ast.walk(tree):
        if isinstance(entry, (ast.ClassDef, ast.FunctionDef)):
            size = lines.count_lines(entry)
            last_line = entry.lineno + size - 1
            if isinstance(source, str):
                source = source.split("\n")
            for i, line in enumerate(source, 1):
                # Print the trailing code as well to make sure
                # we are not missing something.
                if i in range(entry.lineno, last_line + 4):
                    if i == entry.lineno:
                        print("%3s %s" % (size, line))
                    else:
                        print("%3s %s" % (' ', line))
            print("\n\n")


def main():
    filename = sys.argv[1]
    with open(filename) as f:
        source = f.read()
        source = ENCODING_REGEX.sub("", source, count=1)
        tree = ast.parse(source)
        annotate(source, tree)


if __name__ == '__main__':
    main()
