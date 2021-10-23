

def test_categorical(self):
    with ensure_clean_store(self.path) as store:
        _maybe_remove(store, 's')
        s = Series(Categorical(['a', 'b', 'b', 'a', 'a', 'c'], categories=['a', 'b', 'c', 'd'], ordered=False))
        store.append('s', s, format='table')
        result = store.select('s')
        tm.assert_series_equal(s, result)
        _maybe_remove(store, 's_ordered')
        s = Series(Categorical(['a', 'b', 'b', 'a', 'a', 'c'], categories=['a', 'b', 'c', 'd'], ordered=True))
        store.append('s_ordered', s, format='table')
        result = store.select('s_ordered')
        tm.assert_series_equal(s, result)
        _maybe_remove(store, 'df')
        df = DataFrame({
            's': s,
            'vals': [1, 2, 3, 4, 5, 6],
        })
        store.append('df', df, format='table')
        result = store.select('df')
        tm.assert_frame_equal(result, df)
        _maybe_remove(store, 'si')
        s = Series([1, 1, 2, 2, 3, 4, 5]).astype('category')
        store.append('si', s)
        result = store.select('si')
        tm.assert_series_equal(result, s)
        _maybe_remove(store, 'si2')
        s = Series([1, 1, np.nan, 2, 3, 4, 5]).astype('category')
        store.append('si2', s)
        result = store.select('si2')
        tm.assert_series_equal(result, s)
        _maybe_remove(store, 'df2')
        df2 = df.copy()
        df2['s2'] = Series(list('abcdefg')).astype('category')
        store.append('df2', df2)
        result = store.select('df2')
        tm.assert_frame_equal(result, df2)
        info = store.info()
        assert ('/df2   ' in info)
        assert ('/df2/meta/values_block_1/meta' in info)
        _maybe_remove(store, 's2')
        s = Series(Categorical(['a', 'b', 'b', 'a', 'a', 'c'], categories=['a', 'b', 'c', 'd'], ordered=False))
        store.append('s2', s, format='table')
        result = store.select('s2')
        tm.assert_series_equal(result, s)
        _maybe_remove(store, 'df3')
        store.append('df3', df, data_columns=['s'])
        expected = df[df.s.isin(['b', 'c'])]
        result = store.select('df3', where=['s in ["b","c"]'])
        tm.assert_frame_equal(result, expected)
        expected = df[df.s.isin(['b', 'c'])]
        result = store.select('df3', where=['s = ["b","c"]'])
        tm.assert_frame_equal(result, expected)
        expected = df[df.s.isin(['d'])]
        result = store.select('df3', where=['s in ["d"]'])
        tm.assert_frame_equal(result, expected)
        expected = df[df.s.isin(['f'])]
        result = store.select('df3', where=['s in ["f"]'])
        tm.assert_frame_equal(result, expected)
        store.append('df3', df)
        df = concat([df, df])
        expected = df[df.s.isin(['b', 'c'])]
        result = store.select('df3', where=['s in ["b","c"]'])
        tm.assert_frame_equal(result, expected)
        df3 = df.copy()
        df3['s'].cat.remove_unused_categories(inplace=True)
        with pytest.raises(ValueError):
            store.append('df3', df3)
        result = store.select('df3/meta/s/meta')
        assert (result is not None)
        store.remove('df3')
        with pytest.raises(KeyError):
            store.select('df3/meta/s/meta')
