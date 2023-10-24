import sys

from graphviz_operations import plain_dot_to_canvas, tree_to_graphviz_rawtext, render_dot
from treegen import parse_text_to_tree

import argparse


def call_hierarchy_to_canvas(file_path: str):
    with open(file_path, 'r') as f:
        call_graph = f.read()
        return plain_dot_to_canvas(
            render_dot(
                tree_to_graphviz_rawtext(
                    parse_text_to_tree(call_graph)
                )
            )
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert call hierarchy to obsidian canvas')
    parser.add_argument('-f', '--file-path', type=str, required=True, help='path to call hierarchy file. must be space-indented text file.')
    try:
        args = parser.parse_args()
        v = call_hierarchy_to_canvas(args.file_path)
        print(v)
    except TypeError as e:
        parser.print_help()


