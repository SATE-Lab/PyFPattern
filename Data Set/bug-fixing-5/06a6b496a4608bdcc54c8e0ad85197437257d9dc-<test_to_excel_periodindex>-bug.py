def test_to_excel_periodindex(self, engine, ext, tsframe):
    xp = tsframe.resample('M', kind='period').mean()
    xp.to_excel(self.path, 'sht1')
    reader = ExcelFile(self.path)
    rs = pd.read_excel(reader, 'sht1', index_col=0)
    tm.assert_frame_equal(xp, rs.to_period('M'))