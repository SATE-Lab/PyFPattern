@pytest.mark.skipif(SCIPY_11, reason='SciPy raises on -OO')
def test_docstring_optimization_compat():
    pyexe = ('python3' if (not PLATFORM_WIN) else 'python')
    p = subprocess.Popen((pyexe + ' -OO -c "import statsmodels.api as sm"'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    rc = p.returncode
    assert (rc == 0), out