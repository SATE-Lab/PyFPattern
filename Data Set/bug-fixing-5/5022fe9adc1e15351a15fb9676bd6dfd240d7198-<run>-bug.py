def run(self):
    ' use Runner lib to do SSH things '
    super(PullCLI, self).run()
    now = datetime.datetime.now()
    display.display(now.strftime('Starting Ansible Pull at %F %T'))
    display.display(' '.join(sys.argv))
    node = platform.node()
    host = socket.getfqdn()
    limit_opts = ('localhost,%s,127.0.0.1' % ','.join(set([host, node, host.split('.')[0], node.split('.')[0]])))
    base_opts = '-c local '
    if (self.options.verbosity > 0):
        base_opts += (' -%s' % ''.join(['v' for x in range(0, self.options.verbosity)]))
    if ((not self.options.inventory) or ((',' not in self.options.inventory) and (not os.path.exists(self.options.inventory)))):
        inv_opts = 'localhost,'
    else:
        inv_opts = self.options.inventory
    if (self.options.module_name == 'git'):
        repo_opts = ('name=%s dest=%s' % (self.options.url, self.options.dest))
        if self.options.checkout:
            repo_opts += (' version=%s' % self.options.checkout)
        if self.options.accept_host_key:
            repo_opts += ' accept_hostkey=yes'
        if self.options.private_key_file:
            repo_opts += (' key_file=%s' % self.options.private_key_file)
        if self.options.verify:
            repo_opts += ' verify_commit=yes'
        if (not self.options.fullclone):
            repo_opts += ' depth=1'
    path = module_loader.find_plugin(self.options.module_name)
    if (path is None):
        raise AnsibleOptionsError(("module '%s' not found.\n" % self.options.module_name))
    bin_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    cmd = ('%s/ansible -i "%s" %s -m %s -a "%s" all -l "%s"' % (bin_path, inv_opts, base_opts, self.options.module_name, repo_opts, limit_opts))
    for ev in self.options.extra_vars:
        cmd += (' -e "%s"' % ev)
    if self.options.sleep:
        display.display(('Sleeping for %d seconds...' % self.options.sleep))
        time.sleep(self.options.sleep)
    display.debug('running ansible with VCS module to checkout repo')
    display.vvvv(('EXEC: %s' % cmd))
    (rc, out, err) = run_cmd(cmd, live=True)
    if (rc != 0):
        if self.options.force:
            display.warning('Unable to update repository. Continuing with (forced) run of playbook.')
        else:
            return rc
    elif (self.options.ifchanged and ('"changed": true' not in out)):
        display.display('Repository has not changed, quitting.')
        return 0
    playbook = self.select_playbook(self.options.dest)
    if (playbook is None):
        raise AnsibleOptionsError('Could not find a playbook to run.')
    cmd = ('%s/ansible-playbook %s %s' % (bin_path, base_opts, playbook))
    if self.options.vault_password_file:
        cmd += (' --vault-password-file=%s' % self.options.vault_password_file)
    if self.options.inventory:
        cmd += (' -i "%s"' % self.options.inventory)
    for ev in self.options.extra_vars:
        cmd += (' -e "%s"' % ev)
    if (self.options.ask_sudo_pass or self.options.ask_su_pass or self.options.become_ask_pass):
        cmd += ' --ask-become-pass'
    if self.options.tags:
        cmd += (' -t "%s"' % self.options.tags)
    if self.options.subset:
        cmd += (' -l "%s"' % self.options.subset)
    else:
        cmd += (' -l "%s"' % limit_opts)
    os.chdir(self.options.dest)
    display.debug('running ansible-playbook to do actual work')
    display.debug(('EXEC: %s' % cmd))
    (rc, out, err) = run_cmd(cmd, live=True)
    if self.options.purge:
        os.chdir('/')
        try:
            shutil.rmtree(self.options.dest)
        except Exception as e:
            display.error(('Failed to remove %s: %s' % (self.options.dest, str(e))))
    return rc