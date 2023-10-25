import sys

from graphviz_operations import plain_dot_to_canvas, tree_to_graphviz_rawtext, render_dot
from treegen import parse_text_to_tree

import argparse


def call_hierarchy_to_canvas(text_in: str):
    return plain_dot_to_canvas(
        render_dot(
            tree_to_graphviz_rawtext(
                parse_text_to_tree(text_in)
            )
        )
    )


if __name__ == '__main__':
    if not sys.stdin.isatty():
        text = sys.stdin.read()
        sys.stdout.write(call_hierarchy_to_canvas(text))
        sys.stdout.flush()
        sys.exit(0)

    parser = argparse.ArgumentParser(description='Convert call hierarchy to obsidian canvas')
    parser.add_argument('-f', '--file-path', type=str, required=False, help='path to call hierarchy file. must be space-indented text file.')
    parser.add_argument('text', type=str)
    try:
        args = parser.parse_args()
        if args.file_path:
            with open(args.file_path, 'r') as f:
                print(call_hierarchy_to_canvas(args.file_path))
        elif args.text:
            print(call_hierarchy_to_canvas(args.text))

    except TypeError as e:
        parser.print_help()
        sys.exit(1)

    # v = call_hierarchy_to_canvas('sample-call-graph-2.txt')
    # print(v)


