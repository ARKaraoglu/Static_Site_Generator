import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a textnode", "bold")
        node2 = TextNode("This is a textnode", "bold")
        self.assertEqual(node, node2)

        node3 = TextNode("This is a textnode", "bold", "https://")
        node4 = TextNode("This is a textnode", "bold", "")
        self.assertNotEqual(node3, node4)

        node5 = TextNode("This is a different textnode", "bold")
        node6 = TextNode("This is a textnode", "bold")
        self.assertNotEqual(node5, node6)

        node7 = TextNode("This is a textnode", "bold", "")
        node8 = TextNode("This is a textnode", "bold")
        self.assertNotEqual(node7, node8)

        node9 = TextNode("this is a textnode", "text")
        node10 = TextNode("this is a textnode", "bold")
        self.assertNotEqual(node9, node10)

    def test_repr(self):
        node = TextNode("This is a textnode", "bold")
        self.assertEqual(node.__repr__(), "TextNode(This is a textnode, bold, None)")
        
        node2 = TextNode("This is a textnode", "bold", "")
        self.assertEqual(node2.__repr__(), "TextNode(This is a textnode, bold, )")
        
        node3 = TextNode("This is a textnode", "bold", "https://")
        self.assertEqual(node3.__repr__(), "TextNode(This is a textnode, bold, https://)")
        
        node4 = TextNode("This is a different textnode", "text", "https://")
        self.assertEqual(repr(node4), "TextNode(This is a different textnode, text, https://)")

if __name__ == "__main__":
    unittest.main()

