from __future__ import print_function

import ast
from collections import defaultdict
import sys

from vulture import lines
from vulture.core import ENCODING_REGEX


def annotate(tree):
    line_to_sizes = defaultdict(list)
    for entry in ast.walk(tree):
        # Modules don't have a lineno attribute.
        if hasattr(entry, 'lineno'):
            size = lines.count_lines(entry)
            if size > 1:
                line_to_sizes[entry.lineno].append(size)
    return line_to_sizes


def print_annotated(source, line_to_sizes):
    for i, line in enumerate(source.splitlines(), start=1):
        sizes = '+'.join(str(size) for size in line_to_sizes.get(i, []))
        print("%8s %s" % (sizes, line))


def main():
    filename = sys.argv[1]
    with open(filename) as f:
        source = f.read()
    source = ENCODING_REGEX.sub("", source, count=1)
    tree = ast.parse(source)
    line_to_sizes = annotate(tree)
    print_annotated(source, line_to_sizes)


if __name__ == '__main__':
    main()
