import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag = "p", value = "this is a leafnode", props = {"href": "https://"})
        self.assertEqual(node.to_html(), '<p href="https://">this is a leafnode</p>')

    def test_values(self):
        node = LeafNode(tag = "p", value = "this is a leafnode", props = {"href": "https://"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "this is a leafnode")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://"})

    def test_noTag(self):
        node = LeafNode(tag = None, value = "this is a leafnode", props = {"href": "https://"})
        self.assertEqual(node.to_html(), "this is a leafnode")

    def test_noValue(self):
        node = LeafNode(tag = "div", value = None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_noProps(self):
        node = LeafNode(tag = "div", value = "this is a leafnode")
        self.assertEqual(node.to_html(), "<div>this is a leafnode</div>")

    def test_repr(self):
        node = LeafNode(tag = "p", value = "this is a leafnode", props = {"href": "/"})
        self.assertEqual(repr(node), "LeafNode(p, this is a leafnode, {'href': '/'})")
