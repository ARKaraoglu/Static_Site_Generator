from textnode import TextNode, text_type_bold, text_type_text

def main():
    # TextNode.py start
    textnode1 = TextNode("TextNode1", text_type_text)
    textnode2 = TextNode("TextNode2", text_type_bold, "https://www.boot.dev")

    print("---textnode.py---")
    print(textnode1.__eq__(textnode2))
    print(textnode1.__repr__())
    print(textnode2.__repr__())

    #TextNode.py end

main()
