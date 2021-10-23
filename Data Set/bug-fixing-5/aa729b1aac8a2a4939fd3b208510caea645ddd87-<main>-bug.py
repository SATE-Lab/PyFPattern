def main():
    environ_cp = dict(os.environ)
    check_bazel_version('0.5.4')
    reset_tf_configure_bazelrc()
    cleanup_makefile()
    setup_python(environ_cp)
    run_gen_git_source(environ_cp)
    if is_windows():
        environ_cp['TF_NEED_S3'] = '0'
        environ_cp['TF_NEED_GCP'] = '0'
        environ_cp['TF_NEED_HDFS'] = '0'
        environ_cp['TF_NEED_JEMALLOC'] = '0'
        environ_cp['TF_NEED_OPENCL_SYCL'] = '0'
        environ_cp['TF_NEED_COMPUTECPP'] = '0'
        environ_cp['TF_NEED_OPENCL'] = '0'
        environ_cp['TF_CUDA_CLANG'] = '0'
    if is_macos():
        environ_cp['TF_NEED_JEMALLOC'] = '0'
    set_build_var(environ_cp, 'TF_NEED_JEMALLOC', 'jemalloc as malloc', 'with_jemalloc', True)
    set_build_var(environ_cp, 'TF_NEED_GCP', 'Google Cloud Platform', 'with_gcp_support', True, 'gcp')
    set_build_var(environ_cp, 'TF_NEED_HDFS', 'Hadoop File System', 'with_hdfs_support', True, 'hdfs')
    set_build_var(environ_cp, 'TF_NEED_S3', 'Amazon S3 File System', 'with_s3_support', True, 's3')
    set_build_var(environ_cp, 'TF_ENABLE_XLA', 'XLA JIT', 'with_xla_support', False, 'xla')
    set_build_var(environ_cp, 'TF_NEED_GDR', 'GDR', 'with_gdr_support', False, 'gdr')
    set_build_var(environ_cp, 'TF_NEED_VERBS', 'VERBS', 'with_verbs_support', False, 'verbs')
    set_action_env_var(environ_cp, 'TF_NEED_OPENCL_SYCL', 'OpenCL SYCL', False)
    if (environ_cp.get('TF_NEED_OPENCL_SYCL') == '1'):
        set_host_cxx_compiler(environ_cp)
        set_host_c_compiler(environ_cp)
        set_action_env_var(environ_cp, 'TF_NEED_COMPUTECPP', 'ComputeCPP', True)
        if (environ_cp.get('TF_NEED_COMPUTECPP') == '1'):
            set_computecpp_toolkit_path(environ_cp)
        else:
            set_trisycl_include_dir(environ_cp)
    set_action_env_var(environ_cp, 'TF_NEED_CUDA', 'CUDA', False)
    if ((environ_cp.get('TF_NEED_CUDA') == '1') and ('TF_CUDA_CONFIG_REPO' not in environ_cp)):
        set_tf_cuda_version(environ_cp)
        set_tf_cudnn_version(environ_cp)
        set_tf_cuda_compute_capabilities(environ_cp)
        set_tf_cuda_clang(environ_cp)
        if (environ_cp.get('TF_CUDA_CLANG') == '1'):
            set_clang_cuda_compiler_path(environ_cp)
        elif (not is_windows()):
            set_gcc_host_compiler_path(environ_cp)
        set_other_cuda_vars(environ_cp)
    set_build_var(environ_cp, 'TF_NEED_MPI', 'MPI', 'with_mpi_support', False)
    if (environ_cp.get('TF_NEED_MPI') == '1'):
        set_mpi_home(environ_cp)
        set_other_mpi_vars(environ_cp)
    set_grpc_build_flags()
    set_cc_opt_flags(environ_cp)
    set_mkl()
    set_monolithic()
    set_windows_build_flags()
    create_android_bazelrc_configs()
    if workspace_has_any_android_rule():
        print('The WORKSPACE file has at least one of ["android_sdk_repository", "android_ndk_repository"] already set. Will not ask to help configure the WORKSPACE. Please delete the existing rules to activate the helper.\n')
    elif get_var(environ_cp, 'TF_SET_ANDROID_WORKSPACE', 'android workspace', False, 'Would you like to interactively configure ./WORKSPACE for Android builds?', 'Searching for NDK and SDK installations.', 'Not configuring the WORKSPACE for Android builds.'):
        create_android_ndk_rule(environ_cp)
        create_android_sdk_rule(environ_cp)