import pandas as pd


class TableDataFrame():

    def __init__(self, df):
        self.df = df

    def getTable(self):
        return self.df

    def setTable(self, df):
        self.df = df

    def modifyGroup(self, rows, groupnum):
        """
        Let the user set the group for a list of selected rows.
        returns the modified dataframe
        """
        for row in rows:
            self.df.at[row, 'Fraction_Group'] = groupnum

    def modifyFraction(self, rows, *argv):
        """
        Let the user set the fraction for a list of selected rows.
        enabled, when only parsing one number as fraction
        returns the modified dataframe
        """
        if len(argv) == 1:
            for row in rows:
                self.df.at[row, 'Fraction'] = argv[0]
        elif len(argv) == 2:
            count = 0
            for row in rows:
                fracnum = argv[0] + count
                self.df.at[row, 'Fraction'] = fracnum
                if fracnum >= argv[1]:
                    count = 0
                else:
                    count += 1

    def modifyLabelSample(self, labelnum, continuous):
        """
        Let the user change the multiplicity of the selected rows
        continuous should be boolean if true samplenumber counts
        through for all fraction groups otherwise it will start at
        1 for each fraction group
        """
        # generate new dataframe from rows and copied rows of labels
        ndf = []
        for row in self.df.index:
            for cl in range(labelnum):
                label = cl+1
                self.df.at[row, 'Label'] = label
                dfrow = self.df.loc[[row]]
                ndf.append(dfrow)
        ndf = pd.concat(ndf, ignore_index=True)

        # associate the samplenum to the label
        if continuous:
            prevsample = 0
            for row in ndf.index:
                if (row == 0):
                    samplenum = 1
                    ndf.at[row, 'Sample'] = samplenum
                elif(ndf.at[row, 'Fraction_Group'] !=
                     ndf.at[row-1, 'Fraction_Group']):
                    prevsample = ndf.at[row-1, 'Sample']
                    samplenum = ndf.at[row, 'Label'] + prevsample
                    ndf.at[row, 'Sample'] = samplenum
                else:
                    samplenum = ndf.at[row, 'Label'] + prevsample
                    ndf.at[row, 'Sample'] = samplenum
        else:
            for row in ndf.index:
                samplenum = ndf.at[row, 'Label']
                ndf.at[row, 'Sample'] = samplenum

        self.df = ndf

    def rmvRow(self, rows):
        self.df.drop(rows, inplace=True)
