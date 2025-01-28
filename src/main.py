import os
import shutil
from os.path import isdir, isfile
from markdownblocks import markdown_to_html_node
from htmlnode import HTMLNode

def move_content(sourceDir, destinationDir):
    if destinationDir == "public" and os.path.isdir("public"):
        if sourceDir == "static":
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
        print(f"Destination Directory: {path}")
        fileDest = os.path.join(destinationDir, path.split(f"{sourceDir}/")[1])


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

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    filePaths = move_content(dir_path_content, dest_dir_path)
    
    indexFilePaths = []
    for file in filePaths:
        if "index.md" in file:
            indexFilePaths.append(file)
    
    templateFile = open(template_path, "r")
    templateContent = templateFile.read()
    
    for file in indexFilePaths:


        sourceFile = open(file, "r")
        sourceContent = sourceFile.read()

        destFilePath = file.replace("content", "public")
        
        # Changes the index.md with index.html
        newPath = destFilePath.replace(".md", ".html")
        os.rename(destFilePath, newPath)
        
        htmlString = markdown_to_html_node(sourceContent).to_html()
        title = extract_title(sourceContent)
        
        tempContent = templateContent.replace("{{ Title }}", title)
        destinationContent = tempContent.replace("{{ Content }}", htmlString)

        with open(newPath, "w") as destFile:
            print(destFile)
            destFile.write(destinationContent)

def main():
    print(move_content("static", "public"))
    generate_pages_recursively("content", "template.html", "public")

if __name__ == "__main__":
    main()
