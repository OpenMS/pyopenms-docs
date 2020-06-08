import pandas as pd


class TableModifier:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def modifyGroup(self, rows, groupnum):
        for row in rows:
            self.dataframe.at[row, 'Fraction_Group'] = groupnum

        return self.dataframe

    def modifyFraction(self, rows, fractionnum):
        for row in rows:
            self.dataframe.at[row, 'Fraction'] = fractionnum

        return self.dataframe

    def modifySample(self, rows, samplenum):
        for row in rows:
            self.dataframe.at[row, 'Sample'] = samplenum

        return self.dataframe

    def modifyLabel(self, rows, labelnum):
        for row in rows:
            self.dataframe.at[row, 'Label'] = labelnum

        return self.dataframe

    def searchTable(self, dataframe, searchstring):
        header = list(dataframe.columns.values)
        indexesfound = []
        for col in header:
            indexesfound.append(dataframe[col].str.find(searchstring))

        return indexesfound
    
