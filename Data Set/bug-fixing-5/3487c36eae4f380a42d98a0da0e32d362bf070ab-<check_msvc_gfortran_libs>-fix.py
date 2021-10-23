def check_msvc_gfortran_libs(self, library_dirs, libraries):
    library_paths = []
    for library in libraries:
        for library_dir in library_dirs:
            fullpath = os.path.join(library_dir, (library + '.a'))
            if os.path.isfile(fullpath):
                library_paths.append(fullpath)
                break
        else:
            return None
    basename = self.__class__.__name__
    tmpdir = os.path.join(os.getcwd(), 'build', basename)
    if (not os.path.isdir(tmpdir)):
        os.makedirs(tmpdir)
    info = {
        'library_dirs': [tmpdir],
        'libraries': [basename],
        'language': 'f77',
    }
    fake_lib_file = os.path.join(tmpdir, (basename + '.fobjects'))
    fake_clib_file = os.path.join(tmpdir, (basename + '.cobjects'))
    with open(fake_lib_file, 'w') as f:
        f.write('\n'.join(library_paths))
    with open(fake_clib_file, 'w') as f:
        pass
    return info