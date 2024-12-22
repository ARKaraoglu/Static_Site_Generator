from textnode import TextType, TextNode
from htmlnode import HTMLNode

print("Hello World!")

def main():
    # bold = NodeType BOLD

    textnode1 = TextNode("this is a textnode", TextType.BOLD, "https://www.boot.dev")
    print(textnode1.__repr__())
    
    htmlnode1 = HTMLNode("tag", "value", "children", {"href": "/"})
    print(repr(htmlnode1))
main()
