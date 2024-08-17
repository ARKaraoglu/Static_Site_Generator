from htmlnode import HTMLNode
from leafnode import LeafNode

#NOTE: Children of HTMLNode
#NOTE: Exact opposite of LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, value = None, children = children, props = props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        
        resultString = ""
        for index in self.children:
            if isinstance(index, ParentNode):
                index.to_html()
            else:
                resultString += f"<{self.tag}"      # opening tag e.g. <p
                
                assert self.props is not None
                if len(self.props) > 0:
                    for key, value in self.props.items():
                        resultString += f' {key}="{value}"'
                
                resultString += ">"                 # opening tag closing e.g. >
                
                for node in self.children:          # start of processing children
                    if node.tag == None:
                        resultString += node.value
                    else:
                        resultString += f'<{node.tag}'
                        if node.props is not None:
                            for key, value in node.props.items():
                                resultString += f' {key}="{value}"'
               
                        resultString += f'>{node.value}</{node.tag}>'
                                                    # end of processing children
                resultString += f'</{self.tag}>'    # closing tag e.g. </p>

                return resultString


    def __repr__(self):
        return f'ParentNode({self.tag}, {self.children}, {self.props})'

