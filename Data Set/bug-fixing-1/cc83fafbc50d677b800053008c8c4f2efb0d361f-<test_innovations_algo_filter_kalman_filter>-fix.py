

def test_innovations_algo_filter_kalman_filter(reset_randomstate):
    ar_params = np.array([0.5])
    ma_params = np.array([0.2])
    sigma2 = 1
    endog = np.random.normal(size=10)
    acovf = arma_acovf(np.r_[(1, (- ar_params))], np.r_[(1, ma_params)], nobs=len(endog))
    (theta, v) = innovations_algo(acovf)
    u = innovations_filter(endog, theta)
    llf_obs = ((((- 0.5) * (u ** 2)) / (sigma2 * v)) - (0.5 * np.log(((2 * np.pi) * v))))
    mod = SARIMAX(endog, order=(len(ar_params), 0, len(ma_params)))
    res = mod.filter(np.r_[(ar_params, ma_params, sigma2)])
    atol = (1e-06 if PLATFORM_WIN else 0.0)
    assert_allclose(u, res.forecasts_error[0], rtol=1e-06, atol=atol)
    assert_allclose(theta[1:, 0], res.filter_results.kalman_gain[0, 0, :(- 1)], atol=atol)
    assert_allclose(llf_obs, res.llf_obs, atol=atol)
