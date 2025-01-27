import os
import shutil
from os.path import isdir, isfile
from markdownblocks import markdown_to_html_node
from htmlnode import HTMLNode

def move_content(sourceDir, destinationDir):
    if destinationDir == "public" and os.path.isdir("public"):
        shutil.rmtree(destinationDir)

    initialFileList = os.listdir(sourceDir)
    
    filteredFilePaths = []
    for index in initialFileList:
        if os.path.isfile(f"{sourceDir}/{index}"):
            filteredFilePaths.append(f"{sourceDir}/{index}")
        else:
            if os.path.isdir(f"{sourceDir}/{index}"):
                filteredFilePaths.append(f"{sourceDir}/{index}")
            filteredFilePaths.extend(move_content(f"{sourceDir}/{index}",""))


    if destinationDir == "":
        return filteredFilePaths
    
    for path in filteredFilePaths:
        if os.path.exists(destinationDir) is False:
            os.mkdir(destinationDir)

        fileDest = os.path.join(destinationDir, path.split("static/")[1])


        if os.path.isdir(path):
            os.mkdir(fileDest)

        if os.path.isfile(path):
            shutil.copy(path, fileDest)

    return filteredFilePaths


def extract_title(markdown):
    blocks = markdown.split("\n")
    h1 = ""

    for block in blocks:
        if block.startswith("# "):
            h1 = block
            break

    if h1 == "":
        raise Exception("No Title found!")
    return h1.split(" ", 1)[1]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}\n")

    file = open(from_path, "r")
    contents = file.read()
    
    title = extract_title(contents) 
    
    htmlString = markdown_to_html_node(contents).to_html()

    template = open(template_path, "r")
    templateContent = template.read()

    tempContent = templateContent.replace("{{ Title }}", title)
    finaltemplatecontent = tempContent.replace("{{ Content }}", htmlString)

    with open(f"{dest_path}/index.html", "w") as indexFile:
        indexFile.write(finaltemplatecontent)

    
def main():
    print(move_content("static", "public"))
    generate_page("content/index.md", "template.html", "public")

if __name__ == "__main__":
    main()
