class HTMLNode():
    def __init__(self, tag = None, value= None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        htmlString = ""
        
        # assert self.props is not None
        if self.props == None:
            return ""

        for key, value in self.props.items():
            htmlString += f' {key}="{value}"'
        return htmlString

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError("A LeafNode must have a value")
        elif self.tag == None:
            return f"{self.value}"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        elif self.children == None:
            raise ValueError("ParentNode must have children")
        else:
            htmlString = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                if isinstance(child, ParentNode):
                    htmlString += child.to_html()
                else:
                    htmlString += child.to_html()
            htmlString += f"</{self.tag}>"
            return htmlString
    
    def __repr__(self):
        return f'ParentNode({self.tag}, {self.value}, {self.children}, {self.props})'
    

