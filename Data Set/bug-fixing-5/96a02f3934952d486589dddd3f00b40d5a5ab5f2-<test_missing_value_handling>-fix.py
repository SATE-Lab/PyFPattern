@pytest.mark.parametrize('est, support_sparse', [(MinMaxScaler(), False), (QuantileTransformer(n_quantiles=10, random_state=42), True)])
def test_missing_value_handling(est, support_sparse):
    rng = np.random.RandomState(42)
    X = iris.data.copy()
    n_missing = 50
    X[(rng.randint(X.shape[0], size=n_missing), rng.randint(X.shape[1], size=n_missing))] = np.nan
    (X_train, X_test) = train_test_split(X, random_state=1)
    assert (not np.all(np.isnan(X_train), axis=0).any())
    assert np.any(np.isnan(X_train), axis=0).all()
    assert np.any(np.isnan(X_test), axis=0).all()
    X_test[:, 0] = np.nan
    Xt = est.fit(X_train).transform(X_test)
    assert_array_equal(np.isnan(Xt), np.isnan(X_test))
    Xt_inv = est.inverse_transform(Xt)
    assert_array_equal(np.isnan(Xt_inv), np.isnan(X_test))
    assert_allclose(Xt_inv[(~ np.isnan(Xt_inv))], X_test[(~ np.isnan(X_test))])
    for i in range(X.shape[1]):
        est.fit(_get_valid_samples_by_column(X_train, i))
        Xt_col = est.transform(X_test[:, [i]])
        assert_array_equal(Xt_col, Xt[:, [i]])
        if (not np.isnan(X_test[:, i]).all()):
            Xt_col_nonan = est.transform(_get_valid_samples_by_column(X_test, i))
            assert_array_equal(Xt_col_nonan, Xt_col[(~ np.isnan(Xt_col.squeeze()))])
    if support_sparse:
        est_dense = clone(est)
        est_sparse = clone(est)
        Xt_dense = est_dense.fit(X_train).transform(X_test)
        Xt_inv_dense = est_dense.inverse_transform(Xt_dense)
        for sparse_constructor in (sparse.csr_matrix, sparse.csc_matrix, sparse.bsr_matrix, sparse.coo_matrix, sparse.dia_matrix, sparse.dok_matrix, sparse.lil_matrix):
            Xt_sparse = est_sparse.fit(sparse_constructor(X_train)).transform(sparse_constructor(X_test))
            assert_allclose(Xt_sparse.A, Xt_dense)
            Xt_inv_sparse = est_sparse.inverse_transform(Xt_sparse)
            assert_allclose(Xt_inv_sparse.A, Xt_inv_dense)