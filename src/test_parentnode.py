import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_noTag(self):
        node = ParentNode(tag = None, children = [LeafNode("p", "this is a leafnode")])

        with self.assertRaises(ValueError):
            node.to_html()

    def test_noChildren(self):
        node = ParentNode(tag = "p", children = None, props = {"href": "/"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_values(self):
        node = ParentNode(tag = "div", children = [LeafNode("p", "this is a leafnode")], props = {"href": "/"})
        self.assertTrue(node.tag,  "div")
        self.assertTrue(node.children, LeafNode("p", "this is a leafnode"))
        self.assertTrue(node.props,  {'href': '/'})

    def test_multiChildren(self):

        leafnodeList = [
            LeafNode(tag = "p", value = "this is a leafnode"),
            LeafNode(tag = None, value = "this is a leafnode"),
            LeafNode(tag = "div", value = "this is a leafnode", props = {"href": "/"})
        ]
        node = ParentNode(tag = "p", children = leafnodeList, props = {"src": "/"})

        self.assertTrue(node.to_html(), '<p src="/"><p>this is a leafnode</p>this is a leafnode<div href="/">this is a leafnode</div></p>')

    def test_childParent(self):

        leafnodeList = [
            LeafNode(tag = "p", value = "this is a leafnode"),
            LeafNode(tag = "b", value = "this is a leafnode"),
            LeafNode(tag = "a", value = "this is a leafnode", props = {"href": "/"}),
            ParentNode(tag = "div", children = [LeafNode("a", "this is a leafnode"), LeafNode(tag = "code", value = "this is a leafnode", props = {"src": "/"})])
        ]
        node = ParentNode(tag = "p", children = leafnodeList, props = {"src": "/"})

        self.assertTrue(node.to_html(), '<p><p>this is a leafnode</p><b>this is a leafnode</b><a href="/">this is a leafnode</a><div><a>this is a leafnode</a><code src="/">this is a leafnode</code></div></p>')






if __name__ == "__main__":
    unittest.main()
