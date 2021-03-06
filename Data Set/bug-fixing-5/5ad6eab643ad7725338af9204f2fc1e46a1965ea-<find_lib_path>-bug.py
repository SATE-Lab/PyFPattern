def find_lib_path():
    'Find MXNet dynamic library files.\n\n    Returns\n    -------\n    lib_path : list(string)\n        List of all found path to the libraries.\n    '
    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    api_path = os.path.join(curr_path, '../../lib/')
    cmake_build_path = os.path.join(curr_path, '../../build/Release/')
    dll_path = [curr_path, api_path, cmake_build_path]
    if (os.name == 'nt'):
        dll_path.append(os.path.join(curr_path, '../../build'))
        vs_configuration = 'Release'
        if (platform.architecture()[0] == '64bit'):
            dll_path.append(os.path.join(curr_path, '../../build', vs_configuration))
            dll_path.append(os.path.join(curr_path, '../../windows/x64', vs_configuration))
        else:
            dll_path.append(os.path.join(curr_path, '../../build', vs_configuration))
            dll_path.append(os.path.join(curr_path, '../../windows', vs_configuration))
    elif ((os.name == 'posix') and os.environ.get('LD_LIBRARY_PATH', None)):
        dll_path.extend([p.strip() for p in os.environ['LD_LIBRARY_PATH'].split(':')])
    if (os.name == 'nt'):
        os.environ['PATH'] = ((os.path.dirname(__file__) + ';') + os.environ['PATH'])
        dll_path = [os.path.join(p, 'libmxnet.dll') for p in dll_path]
    elif (platform.system() == 'Darwin'):
        dll_path = ([os.path.join(p, 'libmxnet.dylib') for p in dll_path] + [os.path.join(p, 'libmxnet.so') for p in dll_path])
    else:
        dll_path.append('../../../')
        dll_path = [os.path.join(p, 'libmxnet.so') for p in dll_path]
    lib_path = [p for p in dll_path if (os.path.exists(p) and os.path.isfile(p))]
    if (len(lib_path) == 0):
        raise RuntimeError((('Cannot find the files.\n' + 'List of candidates:\n') + str('\n'.join(dll_path))))
    return lib_path