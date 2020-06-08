import pandas as pd

class TableDataFrame():
    def __init__(self,df):
        self.df = df
    def getTable(self):
        return self.df
    def setTable(self, df):
        self.df = df
