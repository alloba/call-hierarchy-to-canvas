import uuid

import graphviz

from treegen import ParseTreeNode


X_OFFSET = 80
Y_OFFSET = 80
WIDTH_OFFSET = 80
HEIGHT_OFFSET = 80


class DotNode:
    def __init__(self, uid: uuid.UUID, label: str, x: float, y: float, width: float, height: float):
        self.id = uid
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_json_string(self):
        label = self.label
        if not label.startswith('"'):
            label = f'"{self.label}"'
        return f' {{  "type":"text", "text":{label}, "id":"{self.id}", "x": {self.x * X_OFFSET}, "y": {self.y * Y_OFFSET}, "width":{self.width * WIDTH_OFFSET}, "height":{self.height * HEIGHT_OFFSET}  }}'


class DotEdge:
    def __init__(self, uid: uuid.UUID, from_node: uuid.UUID, from_side: str, to_node: uuid.UUID, to_side: str):
        self.id = uid
        self.from_node = from_node
        self.to_node = to_node
        self.from_side = from_side
        self.to_side = to_side

    def to_json_string(self):
        return f' {{ "id":"{self.id}", "fromNode":"{self.from_node}", "fromSide":"{self.from_side}", "toNode":"{self.to_node}", "toSide":"{self.to_side}"  }}'


def tree_to_graphviz_rawtext(node: ParseTreeNode) -> str:
    def tree_walk(child_node: ParseTreeNode) -> str:
        if len(child_node.children) == 0:
            return ''

        text = ''
        for child in child_node.children:
            text += f' "{child_node.text}" -> "{child.text}"\n'

        for child in child_node.children:
            text += tree_walk(child)
        return text

    if len(node.children) == 0:
        return 'digraph {\n rankdir=LR;\n' + f' "{node.text}"\n' + '\n}'
    return 'digraph {\n rankdir=LR;\n' + tree_walk(node) + '\n}'


def render_dot(dot_text: str) -> str:
    graph = graphviz.Source(dot_text)
    return graph.pipe(format='plain').decode('utf-8')


def plain_dot_to_canvas(dot_text: str) -> str:
    lines = dot_text.strip().splitlines()
    nodes = []
    edges = []

    for line in lines:
        if line.startswith('node'):
            nodes.append(DotNode(
                uid=uuid.uuid4(),
                label=line.split(' ')[1],
                x=float(line.split(' ')[2]),  #TODO - this fails when there are spaces in the label text
                y=float(line.split(' ')[3]),
                width=float(line.split(' ')[4]),
                height=float(line.split(' ')[5]),

            ))  # name, label, x, y, width, height

    for line in lines:
        if line.startswith('edge'):
            from_node = [x for x in nodes if x.label == line.split(' ')[1]][0]
            to_node = [x for x in nodes if x.label == line.split(' ')[2]][0]
            edges.append(DotEdge(
                uid=uuid.uuid4(),
                from_node=from_node.id,
                from_side='right',
                to_node=to_node.id,
                to_side='left'
            ))

    splitter = ',\n        '

    return f'''
{{ 
    "nodes": [
        {splitter.join([node.to_json_string() for node in nodes])}
    ],
    "edges": [
        {splitter.join([edge.to_json_string() for edge in edges])}
    ]
}}
'''
