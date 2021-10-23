def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)
    write_version_py()
    if (sys.platform == 'win32'):
        f2py_cmds = ['f2py = numpy.f2py.f2py2e:main']
    else:
        f2py_cmds = ['f2py = numpy.f2py.f2py2e:main', ('f2py%s = numpy.f2py.f2py2e:main' % sys.version_info[:1]), ('f2py%s.%s = numpy.f2py.f2py2e:main' % sys.version_info[:2])]
    metadata = dict(name='numpy', maintainer='NumPy Developers', maintainer_email='numpy-discussion@python.org', description=DOCLINES[0], long_description='\n'.join(DOCLINES[2:]), url='https://www.numpy.org', author='Travis E. Oliphant et al.', download_url='https://pypi.python.org/pypi/numpy', license='BSD', classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f], platforms=['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'], test_suite='nose.collector', cmdclass={
        'sdist': sdist_checked,
    }, python_requires='>=3.5', zip_safe=False, entry_points={
        'console_scripts': f2py_cmds,
    })
    if ('--force' in sys.argv):
        run_build = True
        sys.argv.remove('--force')
    else:
        run_build = parse_setuppy_commands()
    from setuptools import setup
    if run_build:
        from numpy.distutils.core import setup
        cwd = os.path.abspath(os.path.dirname(__file__))
        if (not os.path.exists(os.path.join(cwd, 'PKG-INFO'))):
            generate_cython()
        metadata['configuration'] = configuration
    else:
        metadata['version'] = get_version_info()[0]
    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return