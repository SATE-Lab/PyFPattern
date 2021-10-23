

@pytest.mark.parametrize('n, atol', [(20, 0.001), (5, 1e-08)])
def test_eigs_consistency(n, atol):
    vals = np.arange(1, (n + 1), dtype=np.float64)
    A = spdiags(vals, 0, n, n)
    X = np.random.rand(n, 2)
    (lvals, lvecs) = lobpcg(A, X, largest=True, maxiter=100)
    (vals, vecs) = eigs(A, k=2)
    _check_eigen(A, lvals, lvecs, atol=atol, rtol=0)
    assert_allclose(vals, lvals, atol=1e-14)
