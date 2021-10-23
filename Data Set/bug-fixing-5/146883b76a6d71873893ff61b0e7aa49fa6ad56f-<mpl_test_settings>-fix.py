@pytest.fixture(autouse=True)
def mpl_test_settings(request):
    from matplotlib.testing.decorators import _cleanup_cm
    with _cleanup_cm():
        backend = None
        backend_marker = request.keywords.get('backend')
        if (backend_marker is not None):
            assert (len(backend_marker.args) == 1), "Marker 'backend' must specify 1 backend."
            backend = backend_marker.args[0]
            prev_backend = matplotlib.get_backend()
        style = '_classic_test'
        style_marker = request.keywords.get('style')
        if (style_marker is not None):
            assert (len(style_marker.args) == 1), "Marker 'style' must specify 1 style."
            style = style_marker.args[0]
        matplotlib.testing.setup()
        if (backend is not None):
            import matplotlib.pyplot as plt
            try:
                plt.switch_backend(backend)
            except ImportError as exc:
                if ('cairo' in backend.lower()):
                    pytest.skip('Failed to switch to backend {} ({}).'.format(backend, exc))
                else:
                    raise
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', MatplotlibDeprecationWarning)
            matplotlib.style.use(style)
        try:
            (yield)
        finally:
            if (backend is not None):
                plt.switch_backend(prev_backend)