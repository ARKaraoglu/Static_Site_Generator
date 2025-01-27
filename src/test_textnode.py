import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a textnode", TextType.BOLD)
        node2 = TextNode("this is a textnode", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("this is a textnode", TextType.TEXT)
        node2 = TextNode("this is a textnode", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("this is a textnode", TextType.TEXT, "")
        node2 = TextNode("this is a textnode", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_false3(self):
        node = TextNode("this is a different textnode", TextType.TEXT, "")
        node2 = TextNode("this is a textnode", TextType.TEXT, "")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("this is a textnode", TextType.TEXT, "")
        self.assertEqual('TextNode(this is a textnode, text, )', node.__repr__())

    def test_textnode_to_htmlnode_type_text(self):
        node = TextNode("textnode", TextType.TEXT)
        self.assertEqual("LeafNode(None, textnode, None)", repr(text_node_to_html_node(node)))
    
    def test_textnode_to_htmlnode_type_bold(self):
        node = TextNode("leafnode", TextType.BOLD)
        self.assertEqual("LeafNode(b, leafnode, None)", repr(text_node_to_html_node(node)))

    def test_textnode_to_htmlnode_type_italic(self):
        node = TextNode("italic leafnode", TextType.ITALIC)
        self.assertEqual("LeafNode(i, italic leafnode, None)", repr(text_node_to_html_node(node)))

    def test_textnode_to_htmlnode_type_code(self):
        node = TextNode("code leafnode", TextType.CODE)
        # print(node.__repr__())
        self.assertEqual("LeafNode(code, code leafnode, None)", repr(text_node_to_html_node(node)))
    
    def test_textnode_to_htmlnode_type_link(self):
        node = TextNode("link leafnode", TextType.LINK, "https://www.google.com")
        # print(node.__repr__())
        self.assertEqual("LeafNode(a, link leafnode, {'href': 'https://www.google.com'})", repr(text_node_to_html_node(node)))

    def test_textnode_to_htmlnode_type_image(self):
        node = TextNode("image leafnode", TextType.IMAGE, "img")
        # print(node.__repr__())
        self.assertEqual("LeafNode(img, , {'src': 'img', 'alt': 'image leafnode'})", repr(text_node_to_html_node(node)))
   
if __name__ == "__main__":
    unittest.main()
