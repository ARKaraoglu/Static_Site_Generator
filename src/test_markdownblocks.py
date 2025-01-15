import unittest
from markdownblocks import *

class TestMarkdownToHTML(unittest.TestCase):

    #Test markdown_to_blocks
    def test_markdownblocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

        self.assertEqual([
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ], markdown_to_blocks(md))

    def test_markdownblocks_multiple_new_lines(self):
        md = """
# This is a heading
#This is the heading two

this is a paragraph



* this is a list item
* this is a list item two
* and three
"""

        self.assertEqual([
            "# This is a heading\n#This is the heading two",
            "this is a paragraph",
            "* this is a list item\n* this is a list item two\n* and three"
        ], markdown_to_blocks(md))

    def test_markdownblocks_no_new_lines(self):
        md = """
# This is a heading 
this is a paragraph
* This is a list item
"""

        self.assertEqual(["# This is a heading \nthis is a paragraph\n* This is a list item"], markdown_to_blocks(md))

    #Test block_to_block_types
    def test_block_to_block_types_h1_heading(self):
        md = """
# HEADING
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("heading", block_to_block_types(block))
    
    def test_block_to_block_types_h3_heading(self):
        md = """
### HEADING
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("heading", block_to_block_types(block))

    def test_block_to_block_types_h6_heading(self):
        md = """
###### HEADING
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("heading", block_to_block_types(block))

    def test_block_to_block_types_heading_no_space(self):
        md = """
######HEADING
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("paragraph", block_to_block_types(block))

    def test_block_to_block_types_seven_heading_symbol(self):
        md = """
####### HEADING
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("paragraph", block_to_block_types(block))

    def test_block_to_block_types_code_block(self):
        md = """
```Code Block```
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("code", block_to_block_types(block))
    

    def test_block_to_block_types_code_block_false(self):
        md = """
```Not a Code Block``
"""

        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("paragraph", block_to_block_types(block))

    def test_block_to_block_types_quote_block_one_sentence(self):
        md = """
>asda
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("quote", block_to_block_types(blocks[0]))

    def test_block_to_block_types_quote_block_multiple_sentences(self):
        md = """
> Quote 1
> Quote 2
> Quote 3
> Quote 4
> Quote 5
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("quote", block_to_block_types(blocks[0]))

    def test_block_to_block_types_quote_block_false(self):
        md = """
> Quote 1
> Quote 2
> Quote 3
> Quote 4
Quote 5
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))

    def test_block_to_block_types_unordered_block_two_sentence(self):
        md = """
* Unordered Block One
- Unordered Block Two
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))
    
    def test_block_to_block_types_unordered_block_multiple_sentence(self):
        md = """
* Unordered Block One
- Unordered Block Two
* Unordered Block Three
- Unordered Block Four
- Unordered Block Five
* Unordered Block Six
* Unordered Block Seven
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))
    
    def test_block_to_block_types_unordered_block_false(self):
        md = """
* Unordered Block One
- Unordered Block Two
* Unordered Block Three
- Unordered Block Four
- Unordered Block Five
Unordered Block Six
* Unordered Block Seven
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))

    def test_block_to_block_types_unordered_block_false_no_space(self):
        md = """
* Unordered Block One
- Unordered Block Two
* Unordered Block Three
- Unordered Block Four
- Unordered Block Five
*Unordered Block Six
* Unordered Block Seven
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))

    def test_block_to_block_types_ordered_block_one_sentence(self):
        md = """
1. Ordered List
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("ordered_list", block_to_block_types(blocks[0]))

    def test_block_to_block_types_ordered_block_multiple_sentence(self):
        md = """
1. Ordered List
2. Ordered List
3. Ordered List
4. Ordered List
5. OrderedList
6. here
7. here
8. asdas
9. you can take
10. in my vains
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("ordered_list", block_to_block_types(blocks[0]))
    
    def test_block_to_block_types_ordered_block_no_space_false(self):
        md = """
1. Ordered List
2. Ordered List
3. Ordered List
4. Ordered List
5. OrderedList
6. here
7. here
8.asdas
9. you can take
10. in my vains
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))
    
    def test_block_to_block_types_ordered_block_no_number_increment_false(self):
        md = """
1. Ordered List
2. Ordered List
3. Ordered List
4. Ordered List
5. OrderedList
6. here
7. here
7. asdas
8. you can take
9. in my vains
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual("paragraph", block_to_block_types(blocks[0]))

    def test_block_to_block_types_paragraph_block(self):
        md = """
```This is a paragraph``

> This is a paragraph
this is a paragraph

*this is a paragraph
-this is a paragraph

1. thisis a paragraph
1. this is a paragraph
"""

        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual("paragraph", block_to_block_types(block))

# Markdown to html nodes tests

    # Heading
    def test_markdown_to_html_node_heading(self):
        md = """
# Heading 1
### Heading 3 with *bold* and `code`
###### Heading 6 with `code`
"""
        parentNode = markdown_to_html_node(md)
        assert parentNode.children is not None

        self.assertEqual(parentNode.children[0].tag, MarkdownTypes.HEADING, "parent node should be of type heading")
        headingNode = parentNode.children[0]
        childrenNodes = headingNode.children
        self.assertEqual(len(childrenNodes), 3, "3 lines = 3 nodes")
        # Validate Heading 1
        h1 = childrenNodes[0]
        self.assertEqual(h1.tag, "h1", "first line should be of h1 tag")
        self.assertEqual(len(h1.children), 1, "Should have only 1 children since no inline markdown")
        # Validate Heading 2
        h3 = childrenNodes[1]
        self.assertEqual(h3.tag, "h3", "Second child node should have tag of h3")
        self.assertEqual(len(h3.children), 4, "Should have 4 because 2 inline markdown is present")
        self.assertEqual(h3.children[0].tag, None, "Tag should be paragraph")
        self.assertEqual(h3.children[1].tag, "i", "Tag should be italic")
        self.assertEqual(h3.children[1].value, "bold", "Value should be bold")
        self.assertEqual(h3.children[3].tag, "code", "Tag should be code")
        # Validate Heading 3
        h6 = childrenNodes[2]
        self.assertEqual(h6.tag, "h6", "Third child node should have tag of h3")
        self.assertEqual(len(h6.children), 2, "Should have 2 because 1 inline markdown is present")
        self.assertEqual(h6.children[0].tag, None, "Should be none for leafnode don't have a tag for paragraph text")
        self.assertEqual(h6.children[1].tag, "code", "Should be code")
        self.assertEqual(h6.children[1].value, "code", "Should be saying code")


#     def test_markdown_to_html_node_heading_two(self):
#         md = """
# # Heading 1
# ### Heading 3 with *bold* and `code`
# Heading without number signs
# """
#         nodes = markdown_to_html_node(md)
#         assert nodes.children is not None
#         
#         print(nodes.children[0])
    
    def test_markdown_to_html_node_paragraph(self):
        md = """
This is a paragraph
This is `code` with **bold** and *italic* text.
"""
        parentNode = markdown_to_html_node(md)
        # Validate parent node
        self.assertEqual(parentNode.tag, "div", "should be div")
        
        assert parentNode.children is not None
        paragraphParentNode = parentNode.children[0]
        # Validate paragraph parent node
        self.assertEqual(paragraphParentNode.tag, MarkdownTypes.PARAGRAPH, "Should be paragraph")

        paragraphChildren = paragraphParentNode.children
        self.assertEqual(len(paragraphChildren), 2, "Should be 2")
        # Validate paragraph node 2
        p1 = paragraphChildren[0]
        self.assertEqual(len(p1.children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(p1.tag, "p", "Should be p")
        # Validate paragraph node 2
        p2 = paragraphChildren[1]
        self.assertEqual(len(p2.children), 7, "Should be 7")
        self.assertEqual(p2.children[1].tag, "code", "Should be code")
    
    def test_markdown_to_html_node_unordered_list(self):
        pass
    
    def test_markdown_to_html_node_ordered_list(self):
        pass
    
    def test_markdown_to_html_node_quote(self):
        pass
    
    def test_markdown_to_html_node_code(self):
        pass

    def test_markdown_to_html_node_text_to_children(self):
        pass

    def test_markdown_to_html_node(self):
        pass



