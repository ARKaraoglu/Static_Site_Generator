import unittest
from textnode import TextNode, TextType
from splitdelimiter import (
        split_nodes_delimiter, 
        extract_markdown_images, 
        extract_markdown_links, 
        split_nodes_image, 
        split_nodes_link,
        text_to_textnodes
)
class TestSplitDelimiter(unittest.TestCase):
    
    # split delimiter tests
    def test_splitdelimiter_one_node_bold(self):
        node = TextNode("this is a textnode which has **bold** text.", TextType.TEXT)
        newNodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(TextNode("this is a textnode which has ", TextType.TEXT, None), newNodes[0])
        self.assertEqual(TextNode("bold", TextType.BOLD, None), newNodes[1])
        self.assertEqual(TextNode(" text.", TextType.TEXT, None), newNodes[2])

    def test_splitdelimiter_multiple_nodes(self):
        nodes = [
            TextNode("this is a textnode which has **bold** text.", TextType.TEXT),
            TextNode("this is a textnode which has *italic* text.", TextType.TEXT),
            TextNode("this is a bold textnode", TextType.BOLD) 
        ]
        newNodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(len(newNodes), 5)
        self.assertEqual(TextNode("this is a textnode which has ", TextType.TEXT, None), newNodes[0])
        self.assertEqual(TextNode("bold", TextType.BOLD, None), newNodes[1])
        self.assertEqual(TextNode(" text.", TextType.TEXT, None), newNodes[2])
        self.assertEqual(TextNode("this is a textnode which has *italic* text.", TextType.TEXT), newNodes[3])
        self.assertEqual(TextNode("this is a bold textnode", TextType.BOLD), newNodes[4])

    def test_splitdelimiter_no_closing_delimiter(self):
        node = TextNode("this is a textnode with no closing delimiter for **bold test", TextType.TEXT)

        with self.assertRaises(Exception):
            print(split_nodes_delimiter([node], "**", TextType.BOLD))

    def test_splitdelimiter_multiple_node_italic(self):
        pass
    
    def test_splitdelimiter_multiple_node_code(self):
        nodes = [
            TextNode("this is a textnode with `code part` ", TextType.TEXT),
            TextNode("this is a textnode which has `code` for `python` language.", TextType.TEXT),
            TextNode("this is a `code` textnode", TextType.CODE)
        ]
        newNodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(newNodes), 8)
        self.assertEqual(TextNode("this is a textnode with ", TextType.TEXT),newNodes[0])
        self.assertEqual(TextNode("code part", TextType.CODE),newNodes[1])
        self.assertEqual(TextNode("this is a textnode which has ", TextType.TEXT),newNodes[2])
        self.assertEqual(TextNode("code", TextType.CODE),newNodes[3])
        self.assertEqual(TextNode(" for ", TextType.TEXT),newNodes[4])
        self.assertEqual(TextNode("python", TextType.CODE),newNodes[5])
        self.assertEqual(TextNode(" language.", TextType.TEXT),newNodes[6])
        self.assertEqual(TextNode("this is a `code` textnode", TextType.CODE),newNodes[7])


    def test_splitdelimiter_unmatching_delimiter_text_type(self):
        node = TextNode("this is a textnode that has *italic* text.", TextType.TEXT)
        
        with self.assertRaises(Exception):
            print(split_nodes_delimiter([node], "*", TextType.BOLD))
        with self.assertRaises(Exception):
            print(split_nodes_delimiter([node], "**", TextType.ITALIC))
        with self.assertRaises(Exception):
            print(split_nodes_delimiter([node], "*", TextType.CODE))

    #Extract markdown images
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKa0qIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([('rick roll', 'https://i.imgur.com/aKa0qIh.gif'), ('obi wan' , 'https://i.imgur.com/fJRm4Vk.jpeg')], extract_markdown_images(text))

    def test_extract_markdown_images_two(self):
        text = "![h e y](/)this is a test [hey](asdasd)"
        self.assertEqual([('h e y', '/')], extract_markdown_images(text))

    def test_extract_markdown_images_three(self):
        text = "this does not have markdown images"
        self.assertEqual([], extract_markdown_images(text))

    def test_extract_markdown_images_four(self):
        text = "![hey](/) and ![hey two](/) and lastly ![hey three](/)"
        self.assertEqual([('hey', '/'), ('hey two', '/'), ('hey three', '/')], extract_markdown_images(text))
    
    #Extract markdown links

    def test_extract_markdown_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKa0qIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([('rick roll', 'https://i.imgur.com/aKa0qIh.gif'), ('obi wan' , 'https://i.imgur.com/fJRm4Vk.jpeg')], extract_markdown_links(text))

    def test_extract_markdown_links_two(self):
        text = "![h e y](/)this is a test [hey](asdasd)"
        self.assertEqual([('hey', 'asdasd')], extract_markdown_links(text))

    def test_extract_markdown_links_three(self):
        text = "this does not have markdown images"
        self.assertEqual([], extract_markdown_links(text))

    def test_extract_markdown_links_four(self):
        text = "[hey](/) and [hey two](/) and lastly [hey three](/)"
        self.assertEqual([('hey', '/'), ('hey two', '/'), ('hey three', '/')], extract_markdown_links(text))
    

    # Split Nodes Image
    def test_split_nodes_image(self):
        node = TextNode("there is an embedded image ![here](///) in this textnode.", TextType.TEXT)
        self.assertEqual([TextNode("there is an embedded image ", TextType.TEXT), TextNode("here", TextType.IMAGE, "///"), TextNode(" in this textnode.", TextType.TEXT)], split_nodes_image(node))
    
    def test_split_nodes_image_two(self):
        node = TextNode("![here](/) is an embedded ![asda](/) and [link](///) finally here ![last](/)", TextType.TEXT)
        self.assertEqual([TextNode("here", TextType.IMAGE, "/"), TextNode(" is an embedded ", TextType.TEXT), TextNode("asda", TextType.IMAGE, "/"), TextNode(" and [link](///) finally here ", TextType.TEXT), TextNode("last", TextType.IMAGE, "/")], split_nodes_image(node))

    def test_split_nodes_image_three(self):
        node = TextNode("there are three embedded images starting from here: ![image_one](/), ![image_two](/) and ![image_three](/src).", TextType.TEXT)
        self.assertEqual([TextNode("there are three embedded images starting from here: ", TextType.TEXT), TextNode("image_one", TextType.IMAGE, "/"), TextNode(", ", TextType.TEXT), TextNode("image_two", TextType.IMAGE, "/"), TextNode(" and ", TextType.TEXT), TextNode("image_three", TextType.IMAGE, "/src"), TextNode(".", TextType.TEXT)], split_nodes_image(node))

    def test_split_nodes_image_four(self):
        node = TextNode("no embedded image", TextType.TEXT)
        self.assertEqual([TextNode("no embedded image", TextType.TEXT)], split_nodes_image(node))


    #Split Nodes Link
    def test_split_nodes_link(self):
        node = TextNode("there is an embedded image [here](///) in this textnode.", TextType.TEXT)
        self.assertEqual([TextNode("there is an embedded image ", TextType.TEXT), TextNode("here", TextType.LINK, "///"), TextNode(" in this textnode.", TextType.TEXT)], split_nodes_link(node))
    
    def test_split_nodes_link_two(self):
        node = TextNode("[here](/) is an embedded [asda](/) and ![link](///) finally here [last](/)", TextType.TEXT)
        self.assertEqual([TextNode("here", TextType.LINK, "/"), TextNode(" is an embedded ", TextType.TEXT), TextNode("asda", TextType.LINK, "/"), TextNode(" and ![link](///) finally here ", TextType.TEXT), TextNode("last", TextType.LINK, "/")], split_nodes_link(node))

    def test_split_nodes_link_three(self):
        node = TextNode("there are three embedded images starting from here: [image_one](/), [image_two](/) and [image_three](/src).", TextType.TEXT)
        self.assertEqual([TextNode("there are three embedded images starting from here: ", TextType.TEXT), TextNode("image_one", TextType.LINK, "/"), TextNode(", ", TextType.TEXT), TextNode("image_two", TextType.LINK, "/"), TextNode(" and ", TextType.TEXT), TextNode("image_three", TextType.LINK, "/src"), TextNode(".", TextType.TEXT)], split_nodes_link(node))


    def test_split_nodes_link_four(self):
        node = TextNode("no embedded link", TextType.TEXT)
        self.assertEqual([TextNode("no embedded link", TextType.TEXT)], split_nodes_image(node))
    
    # Text to TextNodes
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([TextNode("This is ", TextType.TEXT),TextNode("text", TextType.BOLD),TextNode(" with an ", TextType.TEXT),TextNode("italic", TextType.ITALIC),TextNode(" word and a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" and an ", TextType.TEXT),TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),TextNode(" and a ", TextType.TEXT),TextNode("link", TextType.LINK, "https://boot.dev")],text_to_textnodes(text))

    def test_text_to_textnodes_two(self):
        text = "![one image](/) and a [link](/). has a **bold** text and a `code block` period."
        self.assertEqual([TextNode("one image", TextType.IMAGE, "/"),TextNode(" and a ", TextType.TEXT),TextNode("link", TextType.LINK, "/"),TextNode(". has a ", TextType.TEXT),TextNode("bold", TextType.BOLD),TextNode(" text and a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" period.", TextType.TEXT),],text_to_textnodes(text))
    def test_text_to_textnodes_three(self):
        text = "this is a text with no delimiters and/or links and images"
        self.assertEqual([TextNode("this is a text with no delimiters and/or links and images", TextType.TEXT)], text_to_textnodes(text))

if __name__ == "__main__":
    unittest.main()
