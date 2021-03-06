def test_params_errors():
    X = [[3, 2], [1, 6]]
    y = [1, 0]
    clf = MLPClassifier
    assert_raises(ValueError, clf(hidden_layer_sizes=(- 1)).fit, X, y)
    assert_raises(ValueError, clf(max_iter=(- 1)).fit, X, y)
    assert_raises(ValueError, clf(shuffle='true').fit, X, y)
    assert_raises(ValueError, clf(alpha=(- 1)).fit, X, y)
    assert_raises(ValueError, clf(learning_rate_init=(- 1)).fit, X, y)
    assert_raises(ValueError, clf(momentum=2).fit, X, y)
    assert_raises(ValueError, clf(momentum=(- 0.5)).fit, X, y)
    assert_raises(ValueError, clf(nesterovs_momentum='invalid').fit, X, y)
    assert_raises(ValueError, clf(early_stopping='invalid').fit, X, y)
    assert_raises(ValueError, clf(validation_fraction=1).fit, X, y)
    assert_raises(ValueError, clf(validation_fraction=(- 0.5)).fit, X, y)
    assert_raises(ValueError, clf(beta_1=1).fit, X, y)
    assert_raises(ValueError, clf(beta_1=(- 0.5)).fit, X, y)
    assert_raises(ValueError, clf(beta_2=1).fit, X, y)
    assert_raises(ValueError, clf(beta_2=(- 0.5)).fit, X, y)
    assert_raises(ValueError, clf(epsilon=(- 0.5)).fit, X, y)
    assert_raises(ValueError, clf(n_iter_no_change=(- 1)).fit, X, y)
    assert_raises(ValueError, clf(solver='hadoken').fit, X, y)
    assert_raises(ValueError, clf(learning_rate='converge').fit, X, y)
    assert_raises(ValueError, clf(activation='cloak').fit, X, y)