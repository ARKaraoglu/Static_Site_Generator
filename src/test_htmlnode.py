import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("tag", "value", "children", {"href": "/"})
        self.assertEqual("HTMLNode(tag, value, children, {'href': '/'})", repr(node))

    def test_repr_no_tag(self):
        node = HTMLNode(None, "value", "children", {"href": "/"})
        self.assertEqual("HTMLNode(None, value, children, {'href': '/'})", repr(node))

    def test_repr_no_value(self):
        node = HTMLNode("tag", None, "children", {"href": "/"})
        self.assertEqual("HTMLNode(tag, None, children, {'href': '/'})", repr(node))
    
    def test_repr_no_children(self):
        node = HTMLNode("tag", "value", None, {"href": "/"})
        self.assertEqual("HTMLNode(tag, value, None, {'href': '/'})", repr(node))
    
    def test_repr_no_props(self):
        node = HTMLNode("tag", "value", "children", None)
        self.assertEqual("HTMLNode(tag, value, children, None)", repr(node))

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    #LeafNode Tests
    def test_repr2(self):
        node = LeafNode(tag = "p", value = "leafnode value", props = {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual("LeafNode(p, leafnode value, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    def test_repr_no_value2(self):
        node = LeafNode(tag = "p", value = None, props = {"href": "/"})
        with self.assertRaises(ValueError):
            node.to_html()


    def test_repr_no_tag2(self):
        node = LeafNode(tag = None, value = "this is a leafnode", props = {"href": "/"})
        self.assertEqual(node.to_html(), "this is a leafnode")

    def test_props_to_html2(self):
        node = LeafNode(tag = "p", value = "leafnode value", props = {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_to_html(self):
        node = LeafNode(tag = "p", value = "leafnode value", props = {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">leafnode value</p>')


    def test_repr3(self):
        childrens = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node = ParentNode("div", childrens, {"href": "/"})
        self.assertEqual("ParentNode(div, None, [LeafNode(b, Bold text, None), LeafNode(None, Normal text, None), LeafNode(i, italic text, None), LeafNode(None, Normal text, None)], {'href': '/'})", repr(node))

    def test_repr_no_tag3(self):
        children = [LeafNode("p", "Normal Text")]
        node = ParentNode(None, children, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr_no_children2(self):
        node = ParentNode("div", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html2(self):
        childrens = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "Normal text")
        ]
        node = ParentNode("div", childrens, {"href": "/"})
        self.assertEqual('<div href="/"><b>Bold text</b>Normal text<i>Italic text</i>Normal text</div>', node.to_html())


    def test_to_html_nested_parent_node(self):
        childrens = [
            ParentNode("p",[
                LeafNode("b", "Bold Text"),
                LeafNode("b", "Second Bold Text"),
                LeafNode(None, "Inner Normal Text")
            ],{"href": "https://www.google.com","target": "_blank"}),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "Normal text")
        ]
        node = ParentNode("div", childrens, {"href": "/"})
        self.assertEqual(f'<div href="/"><p href="https://www.google.com" target="_blank"><b>Bold Text</b><b>Second Bold Text</b>Inner Normal Text</p>Normal text<i>Italic text</i>Normal text</div>', node.to_html())


    def test_to_html_double_nested_parent_node(self):
        childrens = [
            ParentNode("div",[
                ParentNode("div", [
                    LeafNode("p", "Inner Inner Text")
                ], {"href": "/", "target": "/"}),
                LeafNode("b", "Second Bold Text"),
            ],{"href": "https://www.google.com","target": "_blank"}),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "Normal text")
        ]
        node = ParentNode("div", childrens, {"href": "~"})
        self.assertEqual('<div href="~"><div href="https://www.google.com" target="_blank"><div href="/" target="/"><p>Inner Inner Text</p></div><b>Second Bold Text</b></div>Normal text<i>Italic text</i>Normal text</div>', node.to_html())

if __name__ == "__main__":
    unittest.main()
