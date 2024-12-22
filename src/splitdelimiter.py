from textnode import TextType, TextNode
import re

text_type_delimiters = {
    # TextType.TEXT: None,
    TextType.BOLD: "**",
    TextType.ITALIC: "*",
    TextType.CODE: "`",
    # TextType.LINK: "a",
    # TextType.IMAGE: "img"
}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # print(f"Old Nodes: {old_nodes}")
    newNodes = []
    
    if text_type_delimiters[text_type] != delimiter:
        raise Exception(f"Delimiter and Text Type do not match: Input({text_type}:{delimiter}) Expected({text_type}:{text_type_delimiters[text_type]})")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newNodes.append(node)
            break
        
        tempNodeList = node.text.split(delimiter)
        filteredNodes = []

        if len(tempNodeList) % 2 == 0:
            raise Exception(f"Closing delimiter,{delimiter}, not found!")

        for x in range(0, len(tempNodeList)):
            if x % 2 == 0:
                if tempNodeList[x].strip() != "":
                    filteredNodes.append(TextNode(tempNodeList[x], TextType.TEXT))
            else:
                filteredNodes.append(TextNode(tempNodeList[x], text_type))
           
        newNodes.extend(filteredNodes)
    return newNodes

def extract_markdown_images(text):
    regex = r"!\[.*?\]\(.*?\)"
    
    foundImages = re.findall(regex, text)
    filteredImages = []

    for image in foundImages:
        altTextRegex = r"!\[.*?\]"
        urlRegex = r"\(.*?\)"

        altTextSection = re.findall(altTextRegex, image)
        altText = ""
        for index in altTextSection[0]:
            if index == "!" or index == "[" or index == "]":
                continue
            else:
                altText += index

        urlSection = re.findall(urlRegex, image)
        url = ""

        for index in urlSection[0]:
            if index == "(" or index == ")":
                continue
            else:
                url += index
        filteredImages.append((altText, url))
        
    return filteredImages

def extract_markdown_links(text):
    regex = r"(?<!!)\[.*?\]\(.*?\)"

    foundLinks = re.findall(regex, text)
    filteredLinks = []


    for link in foundLinks:
        splitLink = link.split("]")

        unfilteredAnchorText = splitLink[0]
        unfilteredUrl = splitLink[1]

        anchorText = ""
        url = ""
        for index in unfilteredAnchorText:
            if index == "[" or index == "]":
                continue
            else:
                anchorText += index

        for index in unfilteredUrl:
            if index == "(" or index == ")":
                continue
            else:
                url += index
        filteredLinks.append((anchorText, url))
    
    return filteredLinks

def split_nodes_image(old_node):
    regex = r"!\[.*?\]\(.*?\)"
    nodeText = old_node.text

    newNodes = []
    markdownImages = extract_markdown_images(nodeText)
    splitNode = re.split(regex, nodeText)
    
    imagePointer = 0
    splitNodePointer = 0

    # print(markdownImages, splitNode)
    for x in range(0, (len(markdownImages) + len(splitNode))):
        # print(x, imagePointer, splitNodePointer)
        if (x % 2) == 0:
            if splitNode[splitNodePointer] == "":
                splitNodePointer += 1
                continue
            else:
                newNodes.append(TextNode(splitNode[splitNodePointer], TextType.TEXT))
                splitNodePointer += 1
        else:
            altText = markdownImages[imagePointer][0]
            url = markdownImages[imagePointer][1]
            newNodes.append(TextNode(altText, TextType.IMAGE, url))
            imagePointer += 1

    return newNodes


def split_nodes_link(old_node):
    regex = r"(?<!!)\[.*?\]\(.*?\)"
    nodeText = old_node.text

    newNodes = []
    markdownLinks = extract_markdown_links(nodeText)
    splitNode = re.split(regex, nodeText)
    
    linkPointer = 0
    splitNodePointer = 0

    # print(markdownLinks, splitNode)
    for x in range(0, (len(markdownLinks) + len(splitNode))):
        # print(x, linkPointer, splitNodePointer)
        if (x % 2) == 0:
            if splitNode[splitNodePointer] == "":
                splitNodePointer += 1
                continue
            else:
                newNodes.append(TextNode(splitNode[splitNodePointer], TextType.TEXT))
                splitNodePointer += 1
        else:
            anchorText = markdownLinks[linkPointer][0]
            url = markdownLinks[linkPointer][1]
            newNodes.append(TextNode(anchorText, TextType.LINK, url))
            linkPointer += 1

    return newNodes


def text_to_textnodes(text):
    nodes_split_by_delimiters = []
    tempList = []

    nodes_split_by_delimiters.append(TextNode(text, TextType.TEXT))

    for node in nodes_split_by_delimiters:
        if node.text_type != TextType.TEXT:
            tempList.append(node)
        else:
            tempList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.BOLD], TextType.BOLD))
    nodes_split_by_delimiters = tempList
    tempList = []


    for node in nodes_split_by_delimiters:
        if node.text_type != TextType.TEXT:
            tempList.append(node)
        else:
            tempList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.ITALIC], TextType.ITALIC))
    nodes_split_by_delimiters = tempList
    tempList = []

    for node in nodes_split_by_delimiters:
        if node.text_type != TextType.TEXT:
            tempList.append(node)
        else:
            tempList.extend(split_nodes_delimiter([node], text_type_delimiters[TextType.CODE], TextType.CODE))
    nodes_split_by_delimiters = tempList
    # print(nodes_split_by_delimiters)
    tempList = []

    for node in nodes_split_by_delimiters:
        if node.text_type != TextType.TEXT:
            tempList.append(node)
        else:
            tempList.extend(split_nodes_image(node))
    # print(tempList)
    nodes_split_by_delimiters = tempList
    tempList = []

    for node in nodes_split_by_delimiters:
        if node.text_type != TextType.TEXT:
            tempList.append(node)
        else:
            tempList.extend(split_nodes_link(node))
    nodes_split_by_delimiters = tempList
    tempList = []

    return nodes_split_by_delimiters



# class Main():
    # pass
    # node = TextNode("this is a textnode ![markdown image](/)![hey](/) with a markdown image. ![third image](/)", TextType.TEXT)
    # print(split_nodes_image(node))
    # nodeTwo = TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
    # print(split_nodes_link(nodeTwo))
    # text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
# Main()

            
