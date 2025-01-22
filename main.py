import os
import shutil
from os.path import isdir, isfile

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

def main():
    print(move_content("static", "public"))

if __name__ == "__main__":
    main()
