import pandas as pd


class TableDataFrame():

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def getTable(self) -> pd.DataFrame:
        """
        Returns the current dataframe
        """
        return self.df

    def setTable(self, df: pd.DataFrame):
        """
        Sets the dataframe to the given
        """
        self.df = df

    def modifyGroup(self, rows: list, groupnum: int):
        """
        Let the user set the group for a list of selected rows.
        Needs a list of selected rows and the integer to which
        the group is set.
        """
        for row in rows:
            self.df.at[row, 'Fraction_Group'] = groupnum

    def modifyFraction(self, rows: list, *argv: int):
        """
        Let the user set the fraction for a list of selected rows.
        when only one number is given in argv one fraction is set
        to all selected entries, else it will count to from min to max
        and sets the group accordingly.
        Takes a list of selected rows and the number(s) how the fractions
        should be set.
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

    def modifyLabelSample(self, labelnum: int, continuous: bool):
        """
        Let the user change the multiplicity of the selected rows
        continuous should be boolean if true samplenumber counts
        through for all fraction groups otherwise it will start at
        1 for each fraction group
        Takes the number of labels and a boolean, which sets the option
        of continuing the samplenumber over groups.
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

    def rmvRow(self, rows: list):
        """
        Let the user remove a list of rows.
        Takes list of selected rows.
        """
        self.df.drop(rows, inplace=True)
