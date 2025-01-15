from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitdelimiter import split_nodes_image, split_nodes_link, text_type_delimiters, split_nodes_delimiter
from textnode import TextType, TextNode, text_node_to_html_node
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

    # Checking Quote Block
    if ">" in words[0][0]:
        quoteBlock = False
        for group in words:
            if group[0].count(">") > 0:
                quoteBlock = True
            else:
                return MarkdownTypes.PARAGRAPH.value
        if quoteBlock == True:
            return MarkdownTypes.QUOTE.value
    
    # Checking Unordered List Block
    if words[0][0] == "-":
        for word in words:
            if word[0] != "-":
                return MarkdownTypes.PARAGRAPH.value
        return MarkdownTypes.UNORDERED_LIST.value

    if words[0][0] == "*":
        for word in words:
            if word[0] != ("*"):
                return MarkdownTypes.PARAGRAPH.value
        return MarkdownTypes.UNORDERED_LIST.value

    # if "*" in words[0][0] or "-" in words[0][0]:
    #     for x in range(0, len(lines)):
    #         if words[x][0] == "*":
    #             continue
    #         elif words[x][0] == "-":
    #             continue
    #         else:
    #             return MarkdownTypes.PARAGRAPH.value
    #     return MarkdownTypes.UNORDERED_LIST.value

    # Checking Ordered List Block
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
# NOTE: Returns a parent html node with header tag and all headings are in children. Requires further testing.
# NOTE: Returns HTMLNode with tag = header and children = [all heading HTMLNodes with tags as h1...h6 with children that contains all textnodes: text,bold,italic,code,link,image]
def markdown_to_html_node_heading(block):
    print("HEADING START\n")
    parentHeaderNode = HTMLNode(tag = MarkdownTypes.HEADING, value = None, children = None, props = None)
    headings = block.split("\n")
    
    splitHeadings = []
    for heading in headings:
        splitHeadings.append(heading.split(" ", 1))
    print(splitHeadings)
    
    childrenHeaderNodes = []
    for heading in splitHeadings:
        tag = f"h{heading[0].count('#')}"
        text = heading[1]
        header = HTMLNode(tag = tag)
        # textNode = TextNode(heading[1], TextType.TEXT)
        
        childrenNodesList = []
        childrenNodesList.extend(text_to_children(text))
        
        header.children = childrenNodesList
        childrenHeaderNodes.append(header)
        

    parentHeaderNode.children = childrenHeaderNodes
    print(parentHeaderNode)
    print("HEADING END\n")

    return parentHeaderNode

def markdown_to_html_node_paragraph(block):
    print("PARAGRAPH START\n")
    lines = block.split("\n")
    parentParagraphNode = HTMLNode(tag = MarkdownTypes.PARAGRAPH, value = None, children = None, props = None)

    childParagraphNodes = []
    for line in lines:
        paragraphNode = HTMLNode("p", value = None, children = text_to_children(line), props = None)
        childParagraphNodes.append(paragraphNode)
    parentParagraphNode.children = childParagraphNodes
    print(parentParagraphNode)
    print("PARAGRAPH END\n")

    return parentParagraphNode
    
#NOTE: Requires Testing
def markdown_to_html_node_unordered_list(block):
    print("UNORDERED LIST START\n")
    lines = block.split("\n")
    listItemNodes = []
    unorderedListParentNode = HTMLNode(tag = MarkdownTypes.UNORDERED_LIST)

    for line in lines:
        text = line.split(" ", 1)[1]
        print(text)
        nodeChildren = text_to_children(text)
        node = HTMLNode(tag = "li", value = None, children = nodeChildren, props = None)
        listItemNodes.append(node)

    unorderedList = HTMLNode(tag = "ul", value = None, children = listItemNodes, props = None)
    unorderedListParentNode.children = unorderedList
    print(unorderedListParentNode)
    print("UNORDERED LIST END\n")

    return unorderedListParentNode


#NOTE: Requires Testing
def markdown_to_html_node_ordered_list(block):
    print("ORDERED LIST START\n")
    lines = block.split("\n")
    listItemNodes = []
    orderedListParentNode = HTMLNode(tag = MarkdownTypes.ORDERED_LIST)

    for line in lines:
        text = line.split(" ", 1)[1]
        nodeChildren = text_to_children(text)
        node = HTMLNode(tag = "li", value = None, children = nodeChildren, props = None)
        listItemNodes.append(node)

    orderedList = HTMLNode(tag = "ol", value = None, children = listItemNodes, props = None)
    orderedListParentNode.children = orderedList
    print(orderedListParentNode)
    print("ORDERED LIST END\n")

    return orderedListParentNode

    # HTMLNODE -> BLOCKQUOTE -> Inner markdown
#NOTE: Requires Testing
def markdown_to_html_node_quote(block):
    print("QUOTE START\n")
    lines = block.split("\n")
    
    childrenList = []
    for line in lines:
        text = line.split(" ", 1)[1]
        children = text_to_children(text)
        quoteLine = HTMLNode(tag = MarkdownTypes.QUOTE, value = None, children = children, props = None)
        childrenList.append(quoteLine)

    quoteBlockNodeList = HTMLNode(tag = "quoteblock", value = None, children = childrenList, props = None)
    quoteBlockParentNode = HTMLNode(tag = MarkdownTypes.QUOTE, children = quoteBlockNodeList)
    
    print(quoteBlockParentNode)
    print("QUOTE END\n")
    
    return quoteBlockParentNode

# def markdown_to_html_node_image(block):
#     print("IMAGE START\n")
#     lines = block.split("\n")
#     parentImageNode = HTMLNode(tag = "image")
#
#     imageNodeChildren = []
#     for line in lines:
#         imageTextNode = TextNode(text = line, text_type = TextType.TEXT)
#         textnode = split_nodes_image(imageTextNode)
#         leafnode = text_node_to_html_node(textnode)
#         imageNodeChildren.append(leafnode)
#
#     parentImageNode.children = imageNodeChildren
#     print(parentImageNode)
#     print("IMAGE END\n")
#
# def markdown_to_html_node_link(block):
#     print("LINK START\n")
#     lines = block.split("\n")
#     parentLinkNode = HTMLNode(tag = "link")
#     
#     linkNodeChildren = []
#     for line in lines:
#         linkTextNode = TextNode(text = line, text_type = TextType.TEXT)
#         textnode = split_nodes_link(linkTextNode)
#         leafnode = text_node_to_html_node(textnode)
#         linkNodeChildren.append(leafnode)
#
#     parentLinkNode.children = linkNodeChildren
#     
#     print(parentLinkNode)
#     print("LINK END\n")
#     

def markdown_to_html_node_code(block):
    print("CODE START\n")
    filteredText = block.split("```")
    textnode = TextNode(text = filteredText[1], text_type = TextType.CODE)
    htmlnode = text_node_to_html_node(textnode)
    parentCodeBlock = HTMLNode(tag = MarkdownTypes.CODE, value = None, children = htmlnode, props = None)
    
    print(parentCodeBlock)
    print("CODE END\n")
    
    return parentCodeBlock

#NOTE: Completed. Testing required!
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
            elif re.search(imageRegex, node.text):
                print("Image Regex activated")
                bufferList.extend(split_nodes_image(node))
            elif re.search(linkRegex, node.text):
                print("Link Regex activated")
                bufferList.extend(split_nodes_link(node))
            else:
                bufferList.append(node)
        if len(bufferList) == len(nodeList):
            break
        else:
            nodeList.clear()
            nodeList.extend(bufferList)
    print(f"\n{nodeList}\n")
    
    #NOTE:TextNode -> HTMLNode(LeafNode)
    #NOTE:LeafNode = Inline Markdown
    htmlnodeList = []
    for textnode in nodeList:
        htmlnodeList.append(text_node_to_html_node(textnode))
    return htmlnodeList

#TODO: Creating and populating 1 Parent HTMLNode for the entire document
#TODO: Writing Test Cases
def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    print(f"\nblocks: {blocks}")
    parentNode = HTMLNode(tag = "div")
    childNodes = []
    for block in blocks:
        blockType = block_to_block_types(block)
        print(f"block: {block} blockType: {blockType}\n")
        if blockType == MarkdownTypes.HEADING.value:
            node = markdown_to_html_node_heading(block)
            childNodes.append(node)
        elif blockType == MarkdownTypes.PARAGRAPH.value:
            node = markdown_to_html_node_paragraph(block)
            childNodes.append(node)
        elif blockType == MarkdownTypes.UNORDERED_LIST.value:
            node = markdown_to_html_node_unordered_list(block)
            childNodes.append(node)
        elif blockType == MarkdownTypes.ORDERED_LIST.value:
            node = markdown_to_html_node_ordered_list(block)
            childNodes.append(node)
        elif blockType == MarkdownTypes.CODE.value:
            node = markdown_to_html_node_code(block)
            childNodes.append(node)
        elif blockType == MarkdownTypes.QUOTE.value:
            node = markdown_to_html_node_quote(block)
            childNodes.append(node)
        else:
            raise Exception(f"Wrong block type: {blockType}")

    parentNode.children = childNodes
    return parentNode

# md = """
# * Unordered List
# """
#
# blocks = markdown_to_blocks(md)
#
# for block in blocks:
#     print(block_to_block_types(block))


# md = """
# # This is a heading with a *italic* text and a **bold** text.
# ### this is an h3 heading with `code` text and a **bold text** in it.
# ##### this is an ![image alt](/) and a [link alt](//).
#
# this is a paragraph with **bold** text
# this is a paragraph with *italic* text
# and a `code` text.
#
# - unordered list 1
# - unordered **bold** list 2
# - unordered *italic* list 3
# - unordered `code` list 4
#
# * unordered list 1
# * unordered list 2
# * unordered list 3
# * unordered `code` list 4
#
# 1. ordered list 1
# 2. ordered **bold** list 2
# 3. ordered *italic* list 3
# 4. ordered `code` list 4
# """
# md = """
# ![Image text](/)
# ![image two](/)
# ![image three](/)
#
# [link one](/)
# [link two](#)
# [link three](#)
#
# ```
# {
#   "firstName": "John",
#   "lastName": "Smith",
#   "age": 25
# }
# ```
#
#
#
#
#
# """
#
#
# markdown_to_html_node(md)
