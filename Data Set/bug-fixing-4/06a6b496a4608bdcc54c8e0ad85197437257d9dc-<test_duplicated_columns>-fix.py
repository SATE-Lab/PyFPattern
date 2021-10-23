def test_duplicated_columns(self, path):
    df = DataFrame([[1, 2, 3], [1, 2, 3], [1, 2, 3]], columns=['A', 'B', 'B'])
    df.to_excel(path, 'test1')
    expected = DataFrame([[1, 2, 3], [1, 2, 3], [1, 2, 3]], columns=['A', 'B', 'B.1'])
    result = pd.read_excel(path, 'test1', index_col=0)
    tm.assert_frame_equal(result, expected)
    result = pd.read_excel(path, 'test1', index_col=0, mangle_dupe_cols=True)
    tm.assert_frame_equal(result, expected)
    df = DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=['A', 'B', 'A', 'B'])
    df.to_excel(path, 'test1')
    result = pd.read_excel(path, 'test1', index_col=0)
    expected = DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=['A', 'B', 'A.1', 'B.1'])
    tm.assert_frame_equal(result, expected)
    df.to_excel(path, 'test1', index=False, header=False)
    result = pd.read_excel(path, 'test1', header=None)
    expected = DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]])
    tm.assert_frame_equal(result, expected)
    msg = 'Setting mangle_dupe_cols=False is not supported yet'
    with pytest.raises(ValueError, match=msg):
        pd.read_excel(path, 'test1', header=None, mangle_dupe_cols=False)