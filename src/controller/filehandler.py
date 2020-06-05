import os
import glob
import pandas as pd
import re

files = []


class FileHandler:
    def __init__(self, path, files, delimiter):
        self.path = path
        self.files = files
        self.delimiter = delimiter

    def getFiles(self, path):
        os.chdir(path)
        files = glob.glob('*.mzML')
        return files

    def tagfiles(self, files, delimiter):
        tagproperty = {}
        for file in files:
            name = file
            tags = []
            file = file.split(".")[0]
            tags = file.split(delimiter)
            tagproperty[name] = tags
        return tagproperty

    def createRawTable(self, tagdict, inputdir):
        columnregex = ["TR[0-9]+", "F[0-9]+", "S[0-9]+"]
        header = ['Fraction_Group', 'Fraction',
                  'Spectra_Filepath', 'Label', 'Sample']
        index = []
        rows = []
        filenames = tagdict.keys()
        for file in filenames:
            index.append(file)
            filtered_tags = {'Fraction_Group': 0, 'Fraction': 0,
                             'Spectra_Filepath': str(inputdir+file),
                             'Label': 0, 'Sample': 0}
            filetags = tagdict[file]
            for tag in filetags:
                if re.match(columnregex[0], tag):
                    filtered_tags['Fraction_Group'] = tag.split('TR')[1]
                elif re.match(columnregex[1], tag):
                    filtered_tags['Fraction'] = tag.split('F')[1]
                elif re.match(columnregex[2], tag):
                    filtered_tags['Sample'] = tag.split('S')[1]
            rows.append([filtered_tags[i]for i in header])
        rawtable = pd.DataFrame(rows, index=index, columns=header)
        return rawtable


# just for testing
# i = input("filepath: ")
# delimiters = ["_"]
# files = getFiles(i)
# preparedfiles = tagfiles(files, delimiters[0])
# rawtable = createRawTable(preparedfiles, i)
# print(rawtable)
