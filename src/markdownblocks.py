from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitdelimiter import text_type_delimiters, split_nodes_delimiter
from textnode import TextType, TextNode
import re

class MarkdownTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    # print(blocks)
    filteredBlocks = []
    for block in blocks:
        if block == "":
            continue
        else:
            filteredBlocks.append(block.strip())

    return filteredBlocks

def block_to_block_types(block):
    lines = block.split("\n")
    words = []
    for line in lines:
        words.append(line.split(" "))
    
    # print(lines)
    # print(words)
        
    # print(lines, words)
    # Checking Heading Block
    if "#" in words[0][0]:
        if words[0][0].count("#") > 6:
            return MarkdownTypes.PARAGRAPH.value
        else:
            if len(words[0]) > 1:
                return MarkdownTypes.HEADING.value
            else:
                return MarkdownTypes.PARAGRAPH.value

    # Checking Code Block
    if "`" in words[0][0]:
        linesLength= len(lines)
        finalWords = len(words[linesLength - 1])
        # print(len(lines), ))
        if words[0][0].count("`") == 3 and words[linesLength - 1][finalWords - 1].count("`") == 3:
            return MarkdownTypes.CODE.value
        else:
            return MarkdownTypes.PARAGRAPH.value

    #Checking Quote Block
    if ">" in words[0][0]:
        quoteBlock = False
        for group in words:
            if group[0].count(">") > 0:
                quoteBlock = True
            else:
                return MarkdownTypes.PARAGRAPH.value
        if quoteBlock == True:
            return MarkdownTypes.QUOTE.value

    if "*" in words[0][0] or "-" in words[0][0]:
        for x in range(0, len(lines)):
            if words[x][0] == "*":
                continue
            elif words[x][0] == "-":
                continue
            else:
                return MarkdownTypes.PARAGRAPH.value
        return MarkdownTypes.UNORDERED_LIST.value


    if "1." in words[0][0]:
        lineNumber = 1
        for x in range(0, len(lines)):
            # print(words[x][0], lineNumber)
            if words[x][0] == f"{lineNumber}.":
                lineNumber += 1
            else:
                return MarkdownTypes.PARAGRAPH.value
        return MarkdownTypes.ORDERED_LIST.value

    return MarkdownTypes.PARAGRAPH.value
    
    
# Heading                       -> tag = h1-h6
# Paragraph                     -> tag = p
# Italic                        -> tag = i
# Bold                          -> tag = b
# List Item (Ordered/Unordered) -> tags = ol,li / ul,li
# Link                          -> tag = a hyperlink: href
# Image                         -> tag = img alt: value
# Code                          -> tag = code
# Quote                         -> tag = blockquote
# text_to_children for inline markdown
#   Italic
#   Bold
#   link
#   image
# TODO: Creating the Parent Heading HTMLNode
def markdown_to_html_node_heading(block):
    headings = block.split("\n")
    
    splitHeadings = []
    for heading in headings:
        splitHeadings.append(heading.split(" ", 1))
    print(splitHeadings)
    
    headingList = []
    for heading in splitHeadings:
        symbol = f"h{heading[0].count('#')}"
        text = heading[1]
        # textNode = TextNode(heading[1], TextType.TEXT)
        
        splitNodeList = []
        splitNodeList.extend(text_to_children(text))
        
        # if len(textList) > 0:
        #     bufferList = []
        #     for text in textList:
        #         if text_type_delimiter[TextType.ITALIC] in text:
        #             bufferList.extend()
        # print(splitNodeList)
        headingList.append(splitNodeList)
    
        


# TODO: Paragraph Handling
# TODO: UnOrdered List Handling
# TODO: Ordered List Handling
# TODO: Quote Handling
def markdown_to_html_node_paragraph(block):
    pass
def markdown_to_html_node_unordered_list(block):
    pass
def markdown_to_html_node_ordered_list(block):
    pass
def markdown_to_html_node_link(links):
    pass
def markdown_to_html_node_image(images):
    pass
def markdown_to_html_node_code(block):
    pass
def markdown_to_html_node_quote(block):
    pass

# TODO: Image Check
# TODO: Link Check
def text_to_children(text):
    nodeList = []
    imageRegex = r"!\[.*?\]\(.*?\)"
    linkRegex = r"(?<!!)\[.*?\]\(.*?\)"
    node = TextNode(text, TextType.TEXT)
    nodeList.append(node)
    while True:
        bufferList = []
        for node in nodeList:
            if node.text_type != TextType.TEXT:
                bufferList.append(node)
                continue
            
            if text_type_delimiters[TextType.BOLD] in node.text:
                bufferList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.BOLD], TextType.BOLD))
            elif text_type_delimiters[TextType.ITALIC] in node.text:
                bufferList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.ITALIC], TextType.ITALIC))
            elif text_type_delimiters[TextType.CODE] in node.text:
                bufferList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.CODE], TextType.CODE))
            elif re.match(imageRegex, node.text):
                pass
            elif re.match(linkRegex, node.text):
                pass
            else:
                bufferList.append(node)
        if len(bufferList) == len(nodeList):
            break
        else:
            nodeList.clear()
            nodeList.extend(bufferList)

    return nodeList

# TODO: Handling every Block types
# TODO: Creating and populating 1 Parent HTMLNode for the entire document
# TODO: Writing Test Cases
def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    print(f"blocks: {blocks}")
    childNodes = []
    for block in blocks:
        blockType = block_to_block_types(block)
        print(f"block: {block} blockType: {blockType}")
        if blockType == MarkdownTypes.HEADING.value:
            markdown_to_html_node_heading(block)
        elif blockType == MarkdownTypes.PARAGRAPH.value:
            markdown_to_html_node_paragraph(block)
        elif blockType == MarkdownTypes.UNORDERED_LIST.value:
            markdown_to_html_node_unordered_list(block)
        elif blockType == MarkdownTypes.ORDERED_LIST.value:
            markdown_to_html_node_ordered_list(block)
        elif blockType == MarkdownTypes.CODE.value:
            markdown_to_html_node_code(block)
        elif blockType == MarkdownTypes.QUOTE.value:
            markdown_to_html_node_quote(block)
        else:
            raise Exception(f"Wrong block type: {blockType}")

# md = """
# * Unordered List
# """
#
# blocks = markdown_to_blocks(md)
#
# for block in blocks:
#     print(block_to_block_types(block))


md = """
# This is a heading with a *italic* text and a **bold** text
"""

markdown_to_html_node(md)
