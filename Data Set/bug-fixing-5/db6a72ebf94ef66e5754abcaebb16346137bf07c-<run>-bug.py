def run(self, tmp=None, task_vars=None):
    provider = load_provider(eos_provider_spec, self._task.args)
    transport = (provider['transport'] or 'cli')
    display.vvvv(('connection transport is %s' % transport), self._play_context.remote_addr)
    if (transport == 'cli'):
        if (self._play_context.connection == 'local'):
            pc = copy.deepcopy(self._play_context)
            pc.connection = 'network_cli'
            pc.network_os = 'eos'
            pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
            pc.port = int((provider['port'] or self._play_context.port or 22))
            pc.remote_user = (provider['username'] or self._play_context.connection_user)
            pc.password = (provider['password'] or self._play_context.password)
            pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
            pc.timeout = int((provider['timeout'] or C.PERSISTENT_COMMAND_TIMEOUT))
            pc.become = (provider['authorize'] or False)
            if pc.become:
                pc.become_method = 'enable'
            pc.become_pass = provider['auth_pass']
            display.vvv(('using connection plugin %s' % pc.connection), pc.remote_addr)
            connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
            socket_path = connection.run()
            display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
            if (not socket_path):
                return {
                    'failed': True,
                    'msg': ('unable to open shell. Please see: ' + 'https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell'),
                }
            task_vars['ansible_socket'] = socket_path
    else:
        provider['transport'] = 'eapi'
        if (provider.get('host') is None):
            provider['host'] = self._play_context.remote_addr
        if (provider.get('port') is None):
            default_port = (443 if provider['use_ssl'] else 80)
            provider['port'] = int((self._play_context.port or default_port))
        if (provider.get('timeout') is None):
            provider['timeout'] = C.PERSISTENT_COMMAND_TIMEOUT
        if (provider.get('username') is None):
            provider['username'] = self._play_context.connection_user
        if (provider.get('password') is None):
            provider['password'] = self._play_context.password
        if (provider.get('authorize') is None):
            provider['authorize'] = False
        self._task.args['provider'] = provider
    result = super(ActionModule, self).run(tmp, task_vars)
    return result