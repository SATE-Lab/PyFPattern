def run(self, tmp=None, task_vars=None):
    if (self._play_context.connection != 'local'):
        return dict(fail=True, msg=('invalid connection specified, expected connection=local, got %s' % self._play_context.connection))
    provider = self.load_provider()
    pc = copy.deepcopy(self._play_context)
    pc.network_os = 'junos'
    if (self._task.action in ('junos_command', 'junos_netconf', 'junos_config', '_junos_template')):
        pc.connection = 'network_cli'
        pc.port = (provider['port'] or self._play_context.port or 22)
    else:
        pc.connection = 'netconf'
        pc.port = (provider['port'] or self._play_context.port or 830)
    pc.remote_user = (provider['username'] or self._play_context.connection_user)
    pc.password = (provider['password'] or self._play_context.password)
    pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
    pc.timeout = (provider['timeout'] or self._play_context.timeout)
    display.vvv(('using connection plugin %s' % pc.connection))
    connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
    socket_path = self._get_socket_path(pc)
    if (not os.path.exists(socket_path)):
        if (pc.connection == 'netconf'):
            (rc, out, err) = connection.exec_command('open_session()')
        else:
            (rc, out, err) = connection.exec_command('open_shell()')
        if (rc != 0):
            return {
                'failed': True,
                'msg': 'unable to connect to control socket',
            }
    task_vars['ansible_socket'] = socket_path
    result = super(ActionModule, self).run(tmp, task_vars)
    if (pc.connection == 'network_cli'):
        display.vvv('closing cli shell connection', self._play_context.remote_addr)
        (rc, out, err) = connection.exec_command('close_shell()')
    return result