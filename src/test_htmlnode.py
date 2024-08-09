import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://", "alt": "props"})
    
    def test_props_to_html(self):
        node = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://", "alt": "props"})
        self.assertEqual(node.props_to_html(), ' href="https://" alt="props"')

    def test_props_to_html2(self):
        node = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://"})
        self.assertEqual(node.props_to_html(), ' href="https://"')

    def test_props_to_html3(self):
        node = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://", "alt": "props", "key": "props2"})
        self.assertEqual(node.props_to_html(), ' href="https://" alt="props" key="props2"')

    def test_props_to_html4(self):
        node = HTMLNode(tag = "tag", value = "value", children = "children", props = {})
        self.assertEqual(node.props_to_html(), '')

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")

    def test_repr2(self):
        node = HTMLNode(tag = "tag", value = "value", children = "children", props = {"href": "https://", "alt": "props"})
        self.assertEqual(repr(node), "HTMLNode(tag, value, children, {'href': 'https://', 'alt': 'props'})")
    
    def test_values(self):
        node = HTMLNode("div", "I wish I could read", )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)


if __name__ == "__main__":
    unittest.main()
