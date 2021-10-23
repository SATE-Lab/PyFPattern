@pytest.mark.parametrize('box', [(lambda x: list(x)), (lambda x: tuple(x)), (lambda x: np.array(x, dtype='int64'))], ids=['list', 'tuple', 'array'])
def test_consistency_for_boxed(self, box):
    df = DataFrame((np.tile(np.arange(3, dtype='int64'), 6).reshape(6, (- 1)) + 1), columns=['A', 'B', 'C'])
    result = df.apply((lambda x: box([1, 2])), axis=1)
    expected = Series([box([1, 2]) for t in df.itertuples()])
    assert_series_equal(result, expected)
    result = df.apply((lambda x: box([1, 2])), axis=1, result_type='expand')
    expected = DataFrame((np.tile(np.arange(2, dtype='int64'), 6).reshape(6, (- 1)) + 1))
    assert_frame_equal(result, expected)