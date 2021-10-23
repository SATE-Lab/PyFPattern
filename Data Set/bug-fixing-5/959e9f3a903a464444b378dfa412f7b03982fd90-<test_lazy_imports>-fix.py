def test_lazy_imports():
    source = textwrap.dedent("\n    import sys\n\n    import matplotlib.figure\n    import matplotlib.backend_bases\n    import matplotlib.pyplot\n\n    assert 'matplotlib._png' not in sys.modules\n    assert 'matplotlib._tri' not in sys.modules\n    assert 'matplotlib._qhull' not in sys.modules\n    assert 'matplotlib._contour' not in sys.modules\n    assert 'urllib.request' not in sys.modules\n    ")
    subprocess.check_call([sys.executable, '-c', source], env={
        **os.environ,
        'MPLBACKEND': '',
        'MATPLOTLIBRC': os.devnull,
    })