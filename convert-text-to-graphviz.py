from graphviz_operations import plain_dot_to_canvas, tree_to_graphviz_rawtext, render_dot
from treegen import parse_text_to_tree


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

    v = call_hierarchy_to_canvas('sample-call-graph.txt')
    print(v)
