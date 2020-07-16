import os
import sys
import glob
import pandas as pd
import re

files = []


class FileHandler:
    """
    Filehandler class that provides support for file and directory interaction.
    """
    def __init__(self, path: str, files: list, delimiter: str):
        self.path = path
        self.files = files
        self.delimiter = delimiter

    def getFiles(self, path: str) -> list:
        """
        Scans a provided directory and returns a list of all
        the mzML files.
        """
        os.chdir(path)
        files = glob.glob('*.mzML')
        return files

    def tagfiles(self, files: list, delimiter: str = "_"):
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

    def importTable(self, file: str) -> pd.DataFrame:
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

    def exportTable(self, table: pd.DataFrame,
                    filename: str, ftype: str = 'csv') -> bool:
        """
        Exports a panda-dataframe to the specified filetype.
        builds a path from a provided filename, a provided path,
        and the provided filetype.

        Defaults:
        If no path is specified, default is the current working directory.
        If no filetype is specified, default is csv.

        Returns:
        Returns false if specified filetype is not supported.
        Returns true if file was successfully written.
        Returns an error if writing the file failed.
        """

        fullpath = filename
        encodingOption = 'utf-8'
        if ftype == 'tsv':
            separator = "\t"
        elif ftype == 'csv':
            separator = ","
        else:
            return False
        try:
            with open(fullpath, 'w') as fileToWrite:
                fileToWrite.write(table.to_csv(
                    sep=separator, index=False, encoding=encodingOption))
            return True
        except:
            e = sys.exc_info()[0]
            return e

    def createRawTable(self, tagdict: dict, inputdir: str):
        """
        Creates pandas-dataframe from prepared files dictionary, which
        contains the filename and its tags (delimiter is _). Dataframes index
        is integer based, header are the column names. Searches the
        tags for regular expressions to automatically include fraction and
        fraction group from filename.
        Default regex:
        Fraction-Group: FG or G
        Fraction: F
        """
        columnregex = ["FG[0-9]+", "G[0-9]+", "F[0-9]+"]
        header = ['Fraction_Group', 'Fraction',
                  'Spectra_Filepath', 'Label', 'Sample']
        index = []
        rows = []
        filenames = tagdict.keys()
        for file in filenames:
            index.append(file)
            filtered_tags = {'Fraction_Group': 0, 'Fraction': 0,
                             'Spectra_Filepath': str(inputdir + "/" + file),
                             'Label': 0, 'Sample': 0}
            filetags = tagdict[file]
            for tag in filetags:
                if re.match(columnregex[0], tag):
                    filtered_tags['Fraction_Group'] = tag.split('FG')[1]
                elif re.match(columnregex[1], tag):
                    filtered_tags['Fraction_Group'] = tag.split('G')[1]
                elif re.match(columnregex[2], tag):
                    filtered_tags['Fraction'] = tag.split('F')[1]
                else:
                    continue
            rows.append([filtered_tags[i]for i in header])
        rawtable = pd.DataFrame(rows, columns=header)
        return rawtable


# just for testing
# i = input("filepath: ")
# delimiters = ["_"]
# files = getFiles(i)
# preparedfiles = tagfiles(files, delimiters[0])
# rawtable = createRawTable(preparedfiles, i)
# print(rawtable)
