import os
import glob

files = []


def filehandler(path):
    os.chdir(path)
    files = glob.glob('*.mzML')
    return files


def tagfiles(file, delimiter):
    tagproperty = {"name": "", "tags": []}
    tagproperty["name"] = file
    tags = []
    file = file.split(".")[0]
    tags = file.split(delimiter)
    tagproperty["tags"] = tags
    return tagproperty


def getTagsbyFile(files, delimiter):
    n = len(files)
    keys = range(n)
    taglist = []
    for file in files:
        taglist.append(tagfiles(file, delimiter))
    return taglist


# just for testing
i = input("filepath: ")

delimiters = ["_"]
files = filehandler(i)
preparedfiles = getTagsbyFile(files, delimiters[0])
print(preparedfiles)
