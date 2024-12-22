from enum import Enum
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
        
    print(lines, words)
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
    
    

md = """
* Unordered List
"""

blocks = markdown_to_blocks(md)

for block in blocks:
    print(block_to_block_types(block))



