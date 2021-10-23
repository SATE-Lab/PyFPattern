@pytest.mark.parametrize('np_type', [np.float16, np.float32, np.float64])
def test_float_types(self, np_type, path):
    df = DataFrame(np.random.random_sample(10), dtype=np_type)
    df.to_excel(path, 'test1')
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0).astype(np_type)
    tm.assert_frame_equal(df, recons, check_dtype=False)