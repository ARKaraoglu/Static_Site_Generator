from enum import Enum
from htmlnode import HTMLNode, ParentNode
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

# Breaks down a markdown into blocks
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filteredBlocks = []
    for block in blocks:
        if block == "":
            continue
        else:
            filteredBlocks.append(block.strip())

    return filteredBlocks

# Determines the type of markdown block
def block_to_block_types(block):
    lines = block.split("\n")
    words = []
    for line in lines:
        words.append(line.split(" "))
    
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
    # print("HEADING START\n")
    heading = block

    if len(heading.split("\n")) > 1:
        splittedHeading = heading.split("\n")
        raise Exception(f'1 block cannot consist of more than 1 Heading Sentence:\n{splittedHeading}, Length:{len(splittedHeading)}')

    if len(heading) == 1:
        raise ValueError("Heading cannot be empty")
    
    tagTextSplit = heading.split(" ", 1)

    childrenNodesList = []
    tag = f"h{tagTextSplit[0].count('#')}"
    text = tagTextSplit[1]
    childrenNodesList.extend(text_to_children(text))
    
    headingParentNode = ParentNode(tag = tag, children = childrenNodesList)
    return headingParentNode

def markdown_to_html_node_paragraph(block):
    lines = block.split("\n")

    children = []
    for line in lines:
        children.extend(text_to_children(line))
    
    paragraphParentNode = ParentNode("p",  children = children, props = None)
    return paragraphParentNode
    
def markdown_to_html_node_unordered_list(block):
    lines = block.split("\n")
    listItems = []

    for line in lines:
        text = ""
        
        # If line is not empty!
        if len(line) > 1:
            text = line.split(" ", 1)[1]

        nodeChildren = text_to_children(text)
        node = ParentNode(tag = "li", children = nodeChildren, props = None)
        listItems.append(node)

    uListParentNode = ParentNode(tag = "ul", children = listItems, props = None)
    return uListParentNode


def markdown_to_html_node_ordered_list(block):
    lines = block.split("\n")
    listItems = []

    for line in lines:
        text = ""
        
        # If line is not empty!
        if len(line) > 2:
            text = line.split(" ", 1)[1]
        
        nodeChildren = text_to_children(text)
        li = ParentNode(tag = "li", children = nodeChildren, props = None)
        listItems.append(li)

    oListParentNode = ParentNode(tag = "ol", children = listItems, props = None)
    return oListParentNode


    # HTMLNODE -> BLOCKQUOTE -> Inner markdown
def markdown_to_html_node_quote(block):
    lines = block.split("\n")
    
    quoteItems = []
    for line in lines:
        text = ""
        
        # Is line is not empty!
        if len(line) > 1:
            text = line.split(" ", 1)[1]
        
        children = text_to_children(text)
        if len(lines) == 1:
            quoteLine = children[0]
        else:
            quoteLine = ParentNode(tag = "p", children = children, props = None)
        quoteItems.append(quoteLine)

    quoteBlockNodeList = ParentNode(tag = "blockquote", children = quoteItems, props = None)
    return quoteBlockNodeList
    


def markdown_to_html_node_code(block):
    filteredText = block.split("```")
    textnode = TextNode(text = filteredText[1], text_type = TextType.CODE)
    codenode = text_node_to_html_node(textnode)
    parentCodeBlock = ParentNode(tag = "pre", children = [codenode], props = None)
    
    return parentCodeBlock

# Handles inline markdowns like bold italic, code, image and links
# Args:
#       text (string): a line of string 
# Returns:
#       htmlNodeList (htmlNodeList) = A list consisting of args(text) broken down into leafnodes with different text types according to inline markdown it contains.
def text_to_children(text):
    nodeList = []
    imageRegex = r"!\[.*?\]\(.*?\)"
    linkRegex = r"(?<!!)\[.*?\]\(.*?\)"
    node = TextNode(text, TextType.TEXT)
    nodeList.append(node)

    while True:
        bufferList = []
        delimiterActivated = False
        for node in nodeList:
            if node.text_type != TextType.TEXT:
                bufferList.append(node)
                continue
            
            if text_type_delimiters[TextType.BOLD] in node.text:
                bufferList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.BOLD], TextType.BOLD))
                delimiterActivated = True
            elif text_type_delimiters[TextType.ITALIC] in node.text:
                bufferList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.ITALIC], TextType.ITALIC))
                delimiterActivated = True
            elif text_type_delimiters[TextType.CODE] in node.text:
                bufferList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.CODE], TextType.CODE))
                delimiterActivated = True
            elif re.search(imageRegex, node.text):
                bufferList.extend(split_nodes_image(node))
                delimiterActivated = True
            elif re.search(linkRegex, node.text):
                bufferList.extend(split_nodes_link(node))
                delimiterActivated = True
            else:
                bufferList.append(node)
        nodeList.clear()
        nodeList.extend(bufferList)
        if delimiterActivated == False:
            break
    
    #NOTE:TextNode -> HTMLNode(LeafNode)
    #NOTE:LeafNode = Inline Markdown
    htmlnodeList = []
    for textnode in nodeList:
        htmlnodeList.append(text_node_to_html_node(textnode))
    return htmlnodeList

# Turnes markdown text into htmlnodes(ParentNode / LeafNode)
def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    childNodes = []
    for block in blocks:
        blockType = block_to_block_types(block)
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

    parentNode = ParentNode(tag = "div", children = childNodes)
    return parentNode

