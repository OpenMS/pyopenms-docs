import os
import glob
import pandas as pd

files = []


def filehandler(path):
    os.chdir(path)
    files = glob.glob('*.mzML')
    return files


def tagfiles(files, delimiter):
    tagproperty = {}
    for file in files:
        name = file
        tags = []
        file = file.split(".")[0]
        tags = file.split(delimiter)
        tagproperty[name] = tags
    return tagproperty


# just for testing
i = input("filepath: ")

delimiters = ["_"]
files = filehandler(i)
preparedfiles = tagfiles(files, delimiters[0])
print(preparedfiles)
