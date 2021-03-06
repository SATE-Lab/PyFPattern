def test_atol_legacy(self):
    with suppress_warnings() as sup:
        sup.filter(DeprecationWarning, '.*called without specifying.*')
        A = eye(2)
        b = (1e-06 * ones(2))
        (x, info) = gmres(A, b, tol=1e-05)
        assert_array_equal(x, np.zeros(2))
        A = eye(2)
        b = ones(2)
        (x, info) = gmres(A, b, tol=1e-05)
        assert_((np.linalg.norm((A.dot(x) - b)) <= (1e-05 * np.linalg.norm(b))))
        assert_allclose(x, b, atol=0, rtol=1e-08)
        rndm = np.random.RandomState(12345)
        A = rndm.rand(30, 30)
        b = (1e-06 * ones(30))
        (x, info) = gmres(A, b, tol=1e-07, restart=20)
        assert_((np.linalg.norm((A.dot(x) - b)) > 1e-07))
    A = eye(2)
    b = (1e-10 * ones(2))
    (x, info) = gmres(A, b, tol=1e-08, atol=0)
    assert_((np.linalg.norm((A.dot(x) - b)) <= (1e-08 * np.linalg.norm(b))))