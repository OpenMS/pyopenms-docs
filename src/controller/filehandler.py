import os
import sys
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
        """
        Scans a provided directory and returns a list of all the matching files.
        """
        os.chdir(path)
        files = glob.glob('*.mzML')
        return files

    def tagfiles(self, files, delimiter="_"):
        """
        Parses filenames in a list of files by a provided delimiter.
        Default delimiter is _ .
        Returns a list of tags.
        """
        tagproperty = {}
        for file in files:
            name = file
            tags = []
            file = file.split(".")[0]
            tags = file.split(delimiter)
            tagproperty[name] = tags
        return tagproperty
    
    def importTable(self, file):
        """
        Imports a csv or tsv file and returns a panda-dataframe.
        Returns false if filetype is not tsv or csv.

        """
        ftype = file.split(".")[1]        
        
        if ftype == "csv":
            fimport = pd.read_csv(file)
            
        elif ftype == "tsv":           
            fimport = pd.read_csv(file, sep='\t')
        else: 
            return False
        return fimport

    def exportTable(self, table, filename, path=os.getcwd, ftype='csv'):
        """
        Exports a panda-dataframe to the specified fyletype.
        builds a path from a provided filename, a provided path, and the provided filetype.

        Defaults:
        If no path is specified, default is the current working directory.
        If no filetype is specified, default is csv.

        Returns:
        Returns false if specified filetype is not supported.
        Returns true if file was successfully written.
        Returns an error if writing the file failed.

        """
        fullpath = path + filename + '.' + ftype
        encodingOption = 'utf-8'
        if ftype == 'tsv':
            separator = "\t"
        elif ftype == 'csv':
            separator = ","
        else:
            return False
        try:
            with open(fullpath,'w') as fileToWrite:
                fileToWrite.write(table.to_csv(sep=separator, index=False, encoding=encodingOption))
            return True
        except:
            e = sys.exc_info()[0]
            return e

    def createRawTable(self, tagdict, inputdir):
        """
        
        """
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
