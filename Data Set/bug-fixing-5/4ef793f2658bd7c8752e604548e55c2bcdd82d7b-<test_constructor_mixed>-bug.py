def test_constructor_mixed(self):
    (index, data) = tm.getMixedTypeDict()
    indexed_frame = DataFrame(data, index=index)
    unindexed_frame = DataFrame(data)
    assert (self.mixed_frame['foo'].dtype == np.object_)