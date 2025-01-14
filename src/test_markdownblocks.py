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
        pass

    def test_markdown_to_html_node_heading_two(self):
        pass
    def test_markdown_to_html_node_heading_three(self):
        pass
    
    def test_markdown_to_html_node_paragraph(self):
        pass
    
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



