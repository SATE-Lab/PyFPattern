

@abc.abstractmethod
def write_cells(self, cells, sheet_name=None, startrow=0, startcol=0, freeze_panes=None):
    '\n        Write given formatted cells into Excel an excel sheet\n\n        Parameters\n        ----------\n        cells : generator\n            cell of formatted data to save to Excel sheet\n        sheet_name : string, default None\n            Name of Excel sheet, if None, then use self.cur_sheet\n        startrow : upper left cell row to dump data frame\n        startcol : upper left cell column to dump data frame\n        freeze_panes: integer tuple of length 2\n            contains the bottom-most row and right-most column to freeze\n        '
    pass
