import os
import glob
import pandas as pd
import re

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


def createRawTable(tagdict, inputdir):
    columnregex = ["TR[0-9]+", "F[0-9]+", "S[0-9]+"]
    header = ['Group', 'Fraction',
              'Filepath', 'Label', 'Sample']
    index = []
    rows = []
    filenames = tagdict.keys()
    for file in filenames:
        index.append(file)
        filtered_tags = {'Group': 0, 'Fraction': 0,
                         'Filepath': str(inputdir+file),
                         'Label': 0, 'Sample': 0}
        filetags = tagdict[file]
        for tag in filetags:
            if re.match(columnregex[0], tag):
                filtered_tags['Group'] = tag.split('TR')[1]
            elif re.match(columnregex[1], tag):
                filtered_tags['Fraction'] = tag.split('F')[1]
            elif re.match(columnregex[2], tag):
                filtered_tags['Sample'] = tag.split('S')[1]
        rows.append([filtered_tags[i]for i in header])
    rawtable = pd.DataFrame(rows, index=index, columns=header)
    return(rawtable, header, index)


# just for testing
i = input("filepath: ")
delimiters = ["_"]
files = filehandler(i)
preparedfiles = tagfiles(files, delimiters[0])
rawtable, header, index = createRawTable(preparedfiles, i)
print(rawtable)
