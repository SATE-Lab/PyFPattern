@pytest.fixture
def datetime_frame():
    "\n    Fixture for DataFrame of floats with DatetimeIndex\n\n    Columns are ['A', 'B', 'C', 'D']\n\n                       A         B         C         D\n    2000-01-03 -1.122153  0.468535  0.122226  1.693711\n    2000-01-04  0.189378  0.486100  0.007864 -1.216052\n    2000-01-05  0.041401 -0.835752 -0.035279 -0.414357\n    2000-01-06  0.430050  0.894352  0.090719  0.036939\n    2000-01-07 -0.620982 -0.668211 -0.706153  1.466335\n    2000-01-10 -0.752633  0.328434 -0.815325  0.699674\n    2000-01-11 -2.236969  0.615737 -0.829076 -1.196106\n    ...              ...       ...       ...       ...\n    2000-02-03  1.642618 -0.579288  0.046005  1.385249\n    2000-02-04 -0.544873 -1.160962 -0.284071 -1.418351\n    2000-02-07 -2.656149 -0.601387  1.410148  0.444150\n    2000-02-08 -1.201881 -1.289040  0.772992 -1.445300\n    2000-02-09  1.377373  0.398619  1.008453 -0.928207\n    2000-02-10  0.473194 -0.636677  0.984058  0.511519\n    2000-02-11 -0.965556  0.408313 -1.312844 -0.381948\n\n    [30 rows x 4 columns]\n    "
    return DataFrame(tm.getTimeSeriesData())