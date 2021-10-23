

@pytest.mark.parametrize('dt', (np.float64, np.complex128))
def test_simple(self, dt):
    z_r = np.array([0.5, (- 0.5)])
    p_r = np.array([(1j / np.sqrt(2)), ((- 1j) / np.sqrt(2))])
    z_r.sort()
    p_r.sort()
    b = np.poly(z_r).astype(dt)
    a = np.poly(p_r).astype(dt)
    (z, p, k) = tf2zpk(b, a)
    z.sort()
    p.sort()
    assert_array_almost_equal(z, z_r)
    assert_array_almost_equal(p, p_r)
    assert_array_almost_equal(k, 1.0)
    assert (k.dtype == dt)
