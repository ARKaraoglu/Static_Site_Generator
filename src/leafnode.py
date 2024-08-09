from htmlnode import HTMLNode

#NOTE: Child Class (OOP) of HTMLNode
#NOTE: Does not accept children
#NOTE: self.value is mandatory anything else optional

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag = tag, value = value, children = None, props = props)
        self.tag = tag
        self.value = value
        self.props = props


    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode value cannot be None")

        if self.tag == None:
            return self.value

        nodeString = ""
        nodeString += f"<{self.tag}"
        
        if self.props is not None:
            for key, value in self.props.items():
                nodeString += f' {key}="{value}"'

        nodeString += f">{self.value}</{self.tag}>"

        return nodeString

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
            


