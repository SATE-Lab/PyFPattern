

def normalized_mutual_info_score(labels_true, labels_pred, average_method='warn'):
    "Normalized Mutual Information between two clusterings.\n\n    Normalized Mutual Information (NMI) is a normalization of the Mutual\n    Information (MI) score to scale the results between 0 (no mutual\n    information) and 1 (perfect correlation). In this function, mutual\n    information is normalized by some generalized mean of ``H(labels_true)``\n    and ``H(labels_pred))``, defined by the `average_method`.\n\n    This measure is not adjusted for chance. Therefore\n    :func:`adjusted_mutual_info_score` might be preferred.\n\n    This metric is independent of the absolute values of the labels:\n    a permutation of the class or cluster label values won't change the\n    score value in any way.\n\n    This metric is furthermore symmetric: switching ``label_true`` with\n    ``label_pred`` will return the same score value. This can be useful to\n    measure the agreement of two independent label assignments strategies\n    on the same dataset when the real ground truth is not known.\n\n    Read more in the :ref:`User Guide <mutual_info_score>`.\n\n    Parameters\n    ----------\n    labels_true : int array, shape = [n_samples]\n        A clustering of the data into disjoint subsets.\n\n    labels_pred : array, shape = [n_samples]\n        A clustering of the data into disjoint subsets.\n\n    average_method : string, optional (default: 'warn')\n        How to compute the normalizer in the denominator. Possible options\n        are 'min', 'geometric', 'arithmetic', and 'max'.\n        If 'warn', 'geometric' will be used. The default will change to\n        'arithmetic' in version 0.22.\n\n        .. versionadded:: 0.20\n\n    Returns\n    -------\n    nmi : float\n       score between 0.0 and 1.0. 1.0 stands for perfectly complete labeling\n\n    See also\n    --------\n    v_measure_score: V-Measure (NMI with arithmetic mean option.)\n    adjusted_rand_score: Adjusted Rand Index\n    adjusted_mutual_info_score: Adjusted Mutual Information (adjusted\n        against chance)\n\n    Examples\n    --------\n\n    Perfect labelings are both homogeneous and complete, hence have\n    score 1.0::\n\n      >>> from sklearn.metrics.cluster import normalized_mutual_info_score\n      >>> normalized_mutual_info_score([0, 0, 1, 1], [0, 0, 1, 1])\n      ... # doctest: +SKIP\n      1.0\n      >>> normalized_mutual_info_score([0, 0, 1, 1], [1, 1, 0, 0])\n      ... # doctest: +SKIP\n      1.0\n\n    If classes members are completely split across different clusters,\n    the assignment is totally in-complete, hence the NMI is null::\n\n      >>> normalized_mutual_info_score([0, 0, 0, 0], [0, 1, 2, 3])i\n      ... # doctest: +SKIP\n      0.0\n\n    "
    if (average_method == 'warn'):
        warnings.warn("The behavior of NMI will change in version 0.22. To match the behavior of 'v_measure_score', NMI will use average_method='arithmetic' by default.", FutureWarning)
        average_method = 'geometric'
    (labels_true, labels_pred) = check_clusterings(labels_true, labels_pred)
    classes = np.unique(labels_true)
    clusters = np.unique(labels_pred)
    if ((classes.shape[0] == clusters.shape[0] == 1) or (classes.shape[0] == clusters.shape[0] == 0)):
        return 1.0
    contingency = contingency_matrix(labels_true, labels_pred, sparse=True)
    contingency = contingency.astype(np.float64)
    mi = mutual_info_score(labels_true, labels_pred, contingency=contingency)
    (h_true, h_pred) = (entropy(labels_true), entropy(labels_pred))
    normalizer = _generalized_average(h_true, h_pred, average_method)
    normalizer = max(normalizer, np.finfo('float64').eps)
    nmi = (mi / normalizer)
    return nmi
