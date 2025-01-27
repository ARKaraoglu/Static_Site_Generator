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
"""
        divNode = markdown_to_html_node(md)
        assert divNode.children is not None
        heading = divNode.children[0]

        self.assertEqual(heading.tag, "h1", "Should be h1")
        self.assertEqual(len(heading.children), 1, "Should be 1 since no inline markdown")


    def test_markdown_to_html_node_paragraph(self):
        md = """
This is a paragraph
This is `code` with **bold** and *italic* text.
"""
        parentNode = markdown_to_html_node(md)
        # Validate parent node
        self.assertEqual(parentNode.tag, "div", "should be div")
        
        assert parentNode.children is not None
        paragraph = parentNode.children[0]
        # Validate paragraph parent node
        self.assertEqual(paragraph.tag, "p", "Should be p")

        paragraphChildren = paragraph.children
        # Validate children node
        self.assertEqual(len(paragraphChildren), 8, "Should be 8")
        self.assertEqual(paragraphChildren[2].value, "code", "Should be code")
        self.assertEqual(paragraphChildren[2].tag, "code", "Should be code")
        self.assertEqual(paragraphChildren[6].value, "italic", "Should be italic")
        self.assertEqual(paragraphChildren[6].tag, "i", "Should be italic")
    
    def test_markdown_to_html_node_unordered_list(self):
        md = """
- Unordered 1
- Unordered 2 with **bold**
- Unordered 3 with *italic*
- Unordered 4 with  `code`
- Unordered 5
- Unordered 6
-
- Unordered 7
"""

        md2 = """
* Unordered 1
* Unordered 2 with **bold**
* Unordered 3 with *italic*
* Unordered 4 with  `code`
* Unordered 5
* Unordered 6
*
* Unordered 7
"""
        parentDiv1 = markdown_to_html_node(md)
        parentDiv2 = markdown_to_html_node(md2)
        
        assert parentDiv1.children is not None
        assert parentDiv2.children is not None
        
        ulNode = parentDiv1.children[0]
        ulNode2 = parentDiv2.children[0]

        listItems = ulNode.children
        listItems2 = ulNode2.children
        
        # Validate UL
        self.assertEqual(ulNode.tag, "ul", "should be ul")
        self.assertEqual(ulNode2.tag, "ul", "should be ul")
        
        # Validate List Items
        self.assertEqual(len(listItems), 8, "8 sentences = 8 children")
        self.assertEqual(len(listItems2), 8, "8 sentences = 8 children")
        
        self.assertEqual(len(listItems[0].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems2[0].children), 1, "Should be 1 since no inline markdown")
        
        self.assertEqual(listItems[0].tag, "li", "Should be li")
        self.assertEqual(listItems2[0].tag, "li", "Should be li")

        self.assertEqual(len(listItems[1].children), 2, "Should be 2")
        self.assertEqual(len(listItems[2].children), 2, "Should be 2")
        self.assertEqual(len(listItems[3].children), 2, "Should be 2")
        self.assertEqual(len(listItems[4].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems[5].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems[6].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems[7].children), 1, "Should be 1 since no inline markdown")

        self.assertEqual(len(listItems2[1].children), 2, "Should be 2")
        self.assertEqual(len(listItems2[2].children), 2, "Should be 2")
        self.assertEqual(len(listItems2[3].children), 2, "Should be 2")
        self.assertEqual(len(listItems2[4].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems2[5].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems2[6].children), 1, "Should be 1 since no inline markdown")
        self.assertEqual(len(listItems2[7].children), 1, "Should be 1 since no inline markdown")
 
    def test_markdown_to_html_node_ordered_list(self):
        md = """
1. Ordered list 1
2. Ordered list 2
3. ordered list **bold** **bold** **bold**3
4.
5.
6.
7.

"""
        parentDiv = markdown_to_html_node(md)
        
        assert parentDiv.children is not None
        olNode = parentDiv.children[0]
        listItems = olNode.children
        
        # Validating olNode
        self.assertEqual(olNode.tag, "ol", "should be ol")
        self.assertEqual(len(olNode.children), 7, "should be 7")

        # Validating List Items
        self.assertEqual(len(listItems[0].children), 1, "Should be 1")
        self.assertEqual(listItems[0].children[0].value, "Ordered list 1", "Should be the sentence itself")
        
        self.assertEqual(len(listItems[1].children), 1, "Should be 1")
        self.assertEqual(listItems[1].children[0].value, "Ordered list 2", "Should be the sentence itself")

        self.assertEqual(len(listItems[2].children), 5, "Should be 5")
        self.assertEqual(listItems[2].children[1].value, "bold", "Should be bold")
        self.assertEqual(listItems[2].children[2].value, "bold", "Should be bold")
        self.assertEqual(listItems[2].children[3].value, "bold", "Should be bold")
        self.assertEqual(listItems[2].children[4].value, "3", "Should be 3")

        self.assertEqual(len(listItems[3].children), 1, "Should be 1")
        self.assertEqual(listItems[3].children[0].value, "", "Should be an empty string")

        self.assertEqual(len(listItems[4].children), 1, "Should be 1")
        self.assertEqual(listItems[4].children[0].value, "", "Should be an empty string")


        self.assertEqual(len(listItems[5].children), 1, "Should be 1")
        self.assertEqual(listItems[5].children[0].value, "", "Should be an empty string")
        
        self.assertEqual(len(listItems[6].children), 1, "Should be 1")
        self.assertEqual(listItems[6].children[0].value, "", "Should be an empty string")
    
    def test_markdown_to_html_node_quote(self):
        md = """
> Quote 1
> Quote 2
> Quote 3 with **bold** and *italic* text.
> Quote 4 has `code` in it.
>
> Quote 5
>
"""
        parentDiv = markdown_to_html_node(md)
        assert parentDiv.children is not None
        
        quoteNode = parentDiv.children[0]        
        quoteChildren = quoteNode.children
        
        # Validating Quote Items
        self.assertEqual(len(quoteChildren), 7, "Should be 7")

        self.assertEqual(len(quoteChildren[2].children), 5, "Should be 5")
        self.assertEqual(quoteChildren[4].children[0].value, "", "Should be empty string")

    
    def test_markdown_to_html_node_code(self):
        md = """
```
def main():
    print("Hello")
main()
```
"""


        parentDiv = markdown_to_html_node(md)

        assert parentDiv.children is not None
        
        codeNode = parentDiv.children[0]
        codeChildren = codeNode.children
        testValue = """
def main():
    print("Hello")
main()
"""
        self.assertEqual(codeChildren[0].value, testValue, "Should be equal")


    def test_markdown_to_html_node(self):
        md = """
# Sample Document

This is a **paragraph** with some *italic* text and a `code` inline. Notice how **bold** and *italic* can combine into **bold word**.

* Unordered list item 1
* Unordered list item 2
* Unordered list item 3

1. Ordered list item 1
2. Ordered list item 2
3. Ordered list item 3
4. Ordered list item 4

> This is a blockquote, intended to be emphasized. 
> 
> It also includes a list item.
>

```
def example_function():
    print("Hello, World!")
```



"""

        parentDivNode = markdown_to_html_node(md)

        assert parentDivNode.children is not None
        nodes = parentDivNode.children

        self.assertEqual(len(nodes), 6, "Should be 6")
