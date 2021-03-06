def main():
    arg_spec = dict(name=dict(required=True), timeout=dict(default=300, type='int'), state=dict(required=True, choices=['present', 'started', 'restarted', 'stopped', 'monitored', 'unmonitored', 'reloaded']))
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    timeout = module.params['timeout']
    MONIT = module.get_bin_path('monit', True)

    def status():
        'Return the status of the process in monit, or the empty string if not present.'
        (rc, out, err) = module.run_command(('%s summary' % MONIT), check_rc=True)
        for line in out.split('\n'):
            parts = line.split()
            if ((len(parts) > 2) and (parts[0].lower() == 'process') and (parts[1] == ("'%s'" % name))):
                return ' '.join(parts[2:]).lower()
        else:
            return ''

    def run_command(command):
        'Runs a monit command, and returns the new status.'
        module.run_command(('%s %s %s' % (MONIT, command, name)), check_rc=True)
        return status()

    def wait_for_monit_to_stop_pending():
        "Fails this run if there is no status or it's pending/initializing for timeout"
        timeout_time = (time.time() + timeout)
        sleep_time = 5
        running_status = status()
        while ((running_status == '') or ('pending' in running_status) or ('initializing' in running_status)):
            if (time.time() >= timeout_time):
                module.fail_json(msg='waited too long for "pending", or "initiating" status to go away ({0})'.format(running_status), state=state)
            time.sleep(sleep_time)
            running_status = status()
    if (state == 'reloaded'):
        if module.check_mode:
            module.exit_json(changed=True)
        (rc, out, err) = module.run_command(('%s reload' % MONIT))
        if (rc != 0):
            module.fail_json(msg='monit reload failed', stdout=out, stderr=err)
        wait_for_monit_to_stop_pending()
        module.exit_json(changed=True, name=name, state=state)
    present = (status() != '')
    if ((not present) and (not (state == 'present'))):
        module.fail_json(msg=('%s process not presently configured with monit' % name), name=name, state=state)
    if (state == 'present'):
        if (not present):
            if module.check_mode:
                module.exit_json(changed=True)
            status = run_command('reload')
            if (status == ''):
                wait_for_monit_to_stop_pending()
            module.exit_json(changed=True, name=name, state=state)
        module.exit_json(changed=False, name=name, state=state)
    wait_for_monit_to_stop_pending()
    running = ('running' in status())
    if (running and (state in ['started', 'monitored'])):
        module.exit_json(changed=False, name=name, state=state)
    if (running and (state == 'stopped')):
        if module.check_mode:
            module.exit_json(changed=True)
        status = run_command('stop')
        if ((status in ['not monitored']) or ('stop pending' in status)):
            module.exit_json(changed=True, name=name, state=state)
        module.fail_json(msg=('%s process not stopped' % name), status=status)
    if (running and (state == 'unmonitored')):
        if module.check_mode:
            module.exit_json(changed=True)
        status = run_command('unmonitor')
        if ((status in ['not monitored']) or ('unmonitor pending' in status)):
            module.exit_json(changed=True, name=name, state=state)
        module.fail_json(msg=('%s process not unmonitored' % name), status=status)
    elif (state == 'restarted'):
        if module.check_mode:
            module.exit_json(changed=True)
        status = run_command('restart')
        if ((status in ['initializing', 'running']) or ('restart pending' in status)):
            module.exit_json(changed=True, name=name, state=state)
        module.fail_json(msg=('%s process not restarted' % name), status=status)
    elif ((not running) and (state == 'started')):
        if module.check_mode:
            module.exit_json(changed=True)
        status = run_command('start')
        if ((status in ['initializing', 'running']) or ('start pending' in status)):
            module.exit_json(changed=True, name=name, state=state)
        module.fail_json(msg=('%s process not started' % name), status=status)
    elif ((not running) and (state == 'monitored')):
        if module.check_mode:
            module.exit_json(changed=True)
        status = run_command('monitor')
        if (status not in ['not monitored']):
            module.exit_json(changed=True, name=name, state=state)
        module.fail_json(msg=('%s process not monitored' % name), status=status)
    module.exit_json(changed=False, name=name, state=state)