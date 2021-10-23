def run(self, tmp=None, task_vars=None):
    if (self._play_context.connection != 'local'):
        return dict(failed=True, msg=('invalid connection specified, expected connection=local, got %s' % self._play_context.connection))
    provider = self.load_provider()
    pc = copy.deepcopy(self._play_context)
    pc.connection = 'network_cli'
    pc.network_os = 'iosxr'
    pc.port = (provider['port'] or self._play_context.port or 22)
    pc.remote_user = (provider['username'] or self._play_context.connection_user)
    pc.password = (provider['password'] or self._play_context.password)
    pc.timeout = (provider['timeout'] or self._play_context.timeout)
    connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
    socket_path = self._get_socket_path(pc)
    if (not os.path.exists(socket_path)):
        display.vvvv('calling open_shell()', pc.remote_addr)
        (rc, out, err) = connection.exec_command('open_shell()')
        if (rc != 0):
            return {
                'failed': True,
                'msg': 'unable to open shell',
                'rc': rc,
            }
    else:
        (rc, out, err) = connection.exec_command('prompt()')
        while str(out).strip().endswith(')#'):
            display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
            connection.exec_command('exit')
            (rc, out, err) = connection.exec_command('prompt()')
    task_vars['ansible_socket'] = socket_path
    result = super(ActionModule, self).run(tmp, task_vars)
    return result