from textnode import TextNode, text_type_bold, text_type_text
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

def main():
    # TextNode start
    textnode1 = TextNode("TextNode1", text_type_text)
    textnode2 = TextNode("TextNode2", text_type_bold, "https://www.boot.dev")

    print("---textnode.py---")
    print(textnode1.__eq__(textnode2))
    print(textnode1.__repr__())
    print(textnode2.__repr__())

    #TextNode end
    #HTMLNode start
    htmlnode = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://", "alt": "props"})
    
    print("---htmlnode.py---")
    print(htmlnode.__repr__())
    print(htmlnode.props_to_html())
    #HTMLNode end
   
    #LeafNode start
    leafnode = LeafNode(tag = "p", value = "this is a leafnode", props = {"href": "/"})
    
    print("---leafnode.py---")
    print(leafnode.to_html())
    #LeafNode end

    #ParentNode start
    leafnodeList = [
        LeafNode(tag = "p", value = "this is a leafnode"),
        LeafNode(tag = None, value = "this is a leafnode"),
        LeafNode(tag = "div", value = "this is a leafnode", props = {"href": "/"})
    ]
    parentnode = ParentNode(tag = "p", children = leafnodeList, props = {"src": "/"})
    
    print("---parentnode.py---")
    print(parentnode.to_html())
    print(parentnode.__repr__())

    #ParentNode end
    




main()
