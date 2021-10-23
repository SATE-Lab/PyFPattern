def test_shift_int(self):
    ts = self.ts.astype(int)
    shifted = ts.shift(1)
    expected = ts.astype(float).shift(1)
    assert_series_equal(shifted, expected)