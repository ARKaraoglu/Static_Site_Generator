from textnode import TextNode, text_type_bold, text_type_text
from htmlnode import HTMLNode
from leafnode import LeafNode

def main():
    # TextNode.py start
    textnode1 = TextNode("TextNode1", text_type_text)
    textnode2 = TextNode("TextNode2", text_type_bold, "https://www.boot.dev")

    print("---textnode.py---")
    print(textnode1.__eq__(textnode2))
    print(textnode1.__repr__())
    print(textnode2.__repr__())

    #TextNode.py end
    #HTMLNode.py start
    htmlnode = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://", "alt": "props"})
    
    print("---htmlnode.py---")
    print(htmlnode.__repr__())
    print(htmlnode.props_to_html())
    #HTMLNode.py end
   
    #leafnode.py start
    leafnode = LeafNode(tag = "p", value = "this is a leafnode", props = {"href": "/"})
    
    print("---leafnode.py---")
    print(leafnode.to_html())
    #leafnode.py end

main()
