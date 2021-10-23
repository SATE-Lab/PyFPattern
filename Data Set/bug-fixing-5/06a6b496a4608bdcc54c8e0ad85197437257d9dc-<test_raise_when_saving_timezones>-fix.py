@pytest.mark.parametrize('dtype', [None, object])
def test_raise_when_saving_timezones(self, dtype, tz_aware_fixture, path):
    tz = tz_aware_fixture
    data = pd.Timestamp('2019', tz=tz)
    df = DataFrame([data], dtype=dtype)
    with pytest.raises(ValueError, match='Excel does not support'):
        df.to_excel(path)
    data = data.to_pydatetime()
    df = DataFrame([data], dtype=dtype)
    with pytest.raises(ValueError, match='Excel does not support'):
        df.to_excel(path)