from typing import List


class ParseTreeNode:
    offset: int = 4  # how many units of spacing is recognized as one level of indentation
    space_marker: str = ' '  # what character is used for indentation

    def __init__(self, text: str):
        self.text = text
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def does_line_have_equal_indent_level(line: str, indent_level: int) -> bool:
    if indent_level == 0:
        return not line.startswith(ParseTreeNode.space_marker)
    return line.startswith(ParseTreeNode.space_marker * ParseTreeNode.offset * indent_level) and not line[ParseTreeNode.offset * indent_level + 1] == ParseTreeNode.space_marker


def create_node(text_lines: List[str], position, indent_level) -> ParseTreeNode:
    text = text_lines[position].strip()
    node = ParseTreeNode(text)
    children_chunks = []
    for line in text_lines[position + 1:len(text_lines)]:
        if does_line_have_equal_indent_level(line, indent_level):
            break
        if does_line_have_equal_indent_level(line, indent_level + 1):
            children_chunks.append(line)

    children_nodes = []
    for chunk in children_chunks:
        pos = text_lines.index(chunk)
        if pos + 1 == len(text_lines):
            children_nodes.append(ParseTreeNode(chunk.strip()))
            continue
        children_nodes.append(create_node(text_lines, pos, indent_level + 1))

    node.children = children_nodes
    return node


def parse_text_to_tree(input_text: str) -> ParseTreeNode:
    text_lines = input_text.strip('\n').strip(' ').splitlines()
    text_lines = list([line.split('(')[0] for line in text_lines])

    return create_node(text_lines, 0, indent_level=0)



