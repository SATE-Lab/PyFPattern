def test(self, args, targets, python_version):
    '\n        :type args: SanityConfig\n        :type targets: SanityTargets\n        :type python_version: str\n        :rtype: TestResult\n        '
    with open('test/sanity/import/skip.txt', 'r') as skip_fd:
        skip_paths = skip_fd.read().splitlines()
    skip_paths_set = set(skip_paths)
    paths = sorted((i.path for i in targets.include if ((os.path.splitext(i.path)[1] == '.py') and (i.path.startswith('lib/ansible/modules/') or i.path.startswith('lib/ansible/module_utils/')) and (i.path not in skip_paths_set))))
    if (not paths):
        return SanitySkipped(self.name, python_version=python_version)
    env = ansible_environment(args, color=False)
    virtual_environment_path = os.path.abspath(('test/runner/.tox/minimal-py%s' % python_version.replace('.', '')))
    virtual_environment_bin = os.path.join(virtual_environment_path, 'bin')
    remove_tree(virtual_environment_path)
    python = find_python(python_version)
    cmd = [python, '-m', 'virtualenv', virtual_environment_path, '--python', python, '--no-setuptools', '--no-wheel']
    if (not args.coverage):
        cmd.append('--no-pip')
    run_command(args, cmd, capture=True)
    importer_path = os.path.join(virtual_environment_bin, 'importer.py')
    if (not args.explain):
        os.symlink(os.path.abspath('test/sanity/import/importer.py'), importer_path)
    env['PATH'] = ('%s:%s' % (virtual_environment_bin, env['PATH']))
    env['PYTHONPATH'] = os.path.abspath('test/sanity/import/lib')
    if args.coverage:
        run_command(args, generate_pip_install(['pip'], 'sanity.import', packages=['setuptools']), env=env)
        run_command(args, generate_pip_install(['pip'], 'sanity.import', packages=['coverage']), env=env)
        run_command(args, ['pip', 'uninstall', '--disable-pip-version-check', '-y', 'setuptools'], env=env)
        run_command(args, ['pip', 'uninstall', '--disable-pip-version-check', '-y', 'pip'], env=env)
    cmd = ['importer.py']
    data = '\n'.join(paths)
    display.info(data, verbosity=4)
    results = []
    try:
        (stdout, stderr) = intercept_command(args, cmd, data=data, target_name=self.name, env=env, capture=True, python_version=python_version, path=env['PATH'])
        if (stdout or stderr):
            raise SubprocessError(cmd, stdout=stdout, stderr=stderr)
    except SubprocessError as ex:
        if ((ex.status != 10) or ex.stderr or (not ex.stdout)):
            raise
        pattern = '^(?P<path>[^:]*):(?P<line>[0-9]+):(?P<column>[0-9]+): (?P<message>.*)$'
        results = [re.search(pattern, line).groupdict() for line in ex.stdout.splitlines()]
        results = [SanityMessage(message=r['message'], path=r['path'], line=int(r['line']), column=int(r['column'])) for r in results]
        results = [result for result in results if (result.path not in skip_paths)]
    if results:
        return SanityFailure(self.name, messages=results, python_version=python_version)
    return SanitySuccess(self.name, python_version=python_version)