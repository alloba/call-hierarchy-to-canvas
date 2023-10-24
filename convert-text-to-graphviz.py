import uuid
import graphviz
from typing import List


class ParseTreeNode:
    def __init__(self, text: str):
        self.text = text
        self.children = []
    def add_child(self, child_node):
        self.children.append(child_node)


def does_line_have_equal_indent_level(line: str, indent_level: int) -> bool:
    OFFSET = 4  # TODO elevate to global constant
    return line.startswith(' ' * OFFSET * indent_level) and not line[OFFSET * indent_level + 1] == ' '


def create_node(text_lines: List[str], position, indent_level) -> ParseTreeNode:

    text = text_lines[position].strip()
    node = ParseTreeNode(text)
    children_chunks = []
    for line in text_lines[position+1:len(text_lines)]:
        if does_line_have_equal_indent_level(line, indent_level):
            break
        if does_line_have_equal_indent_level(line, indent_level + 1):
            children_chunks.append(line)

    children_nodes = []
    for chunk in children_chunks:
        pos = text_lines.index(chunk)
        if pos+1 == len(text_lines):
            children_nodes.append(ParseTreeNode(chunk.strip()))
            continue
        children_nodes.append(create_node(text_lines, pos, indent_level + 1))

    node.children = children_nodes
    return node


def parse_text_to_tree(input_text: str) -> ParseTreeNode:
    text_lines = input_text.strip('\n').strip(' ').splitlines()
    text_lines = list([line.split('(')[0] for line in text_lines])

    return create_node(text_lines, 0, indent_level=0)


def tree_to_graphviz(node: ParseTreeNode) -> str:
    def tree_walk(child_node: ParseTreeNode) -> str:
        if len(child_node.children) == 0:
            return ''

        text = ''
        for child in child_node.children:
            text += f' "{child_node.text}" -> "{child.text}"\n'

        for child in child_node.children:
            text += tree_walk(child)
        return text

    return 'digraph {\n rankdir=LR;\n' + tree_walk(node) + '\n}'


def plain_dot_to_canvas(dot_text: str) -> str:
    lines = dot_text.strip().splitlines()
    nodes = []
    edges = []
    for line in lines:
        if line.startswith('node'):
            nodes.append([   line.split(' ')[1], line.split(' ')[2], line.split(' ')[3], line.split(' ')[4], line.split(' ')[5], uuid.uuid4()   ]) # name, x, y, width, height, uuid
        if line.startswith('edge'):
            edges.append([line.split(' ')[1], line.split(' ')[2]]) # tail, head

    text = '{\n"nodes": [\n'
    for node in nodes:
        text += f'\n {{  "type":"text", "text":{node[0]}, "id":"{node[5]}", "x": {float(node[1]) * 80}, "y": {float(node[2]) * 80}, "width":{float(node[3]) * 80}, "height":{float(node[4]) * 80}  }},'

    text = text[:-1]  # strip last comma

    text += '],\n"edges": [\n'

    for edge in edges:
        from_node = [x for x in nodes if x[0] == edge[0]][0][5]
        to_node = [x for x in nodes if x[0] == edge[1]][0][5]
        text += f'\n {{ "id":"{uuid.uuid4()}", "fromNode":"{from_node}", "fromSide":"right", "toNode":"{to_node}", "toSide":"left"  }},'
    text = text[:-1]  # strip last comma

    text += ']\n}\n'
    return text


if __name__ == '__main__':
    call_graph = open('sample-call-graph.txt', 'r').read()
    call_graph_tree = parse_text_to_tree(call_graph)
    graphviz_diagram_text = tree_to_graphviz(call_graph_tree)

    graph = graphviz.Source(graphviz_diagram_text)
    v = plain_dot_to_canvas(graph.pipe(format='plain').decode('utf-8'))
    print(v)
