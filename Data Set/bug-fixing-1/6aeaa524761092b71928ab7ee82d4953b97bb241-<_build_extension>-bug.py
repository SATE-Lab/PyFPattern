

def _build_extension(ffi, cffi_wrapper_name, target_dir, verbose):
    try:
        tmpdir = tempfile.mkdtemp()
        ext_suf = ('.pyd' if (os.sys.platform == 'win32') else '.so')
        libname = (cffi_wrapper_name + ext_suf)
        ffi.compile(tmpdir=tmpdir, verbose=verbose, target=libname)
        shutil.copy(os.path.join(tmpdir, libname), os.path.join(target_dir, libname))
    finally:
        shutil.rmtree(tmpdir)
