def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='str', aliases=['unit', 'service']), state=dict(choices=['started', 'stopped', 'restarted', 'reloaded'], type='str'), enabled=dict(type='bool'), masked=dict(type='bool'), daemon_reload=dict(type='bool', default=False, aliases=['daemon-reload']), user=dict(type='bool', default=False)), supports_check_mode=True, required_one_of=[['state', 'enabled', 'masked', 'daemon_reload']])
    systemctl = module.get_bin_path('systemctl')
    if module.params['user']:
        systemctl = (systemctl + ' --user')
    unit = module.params['name']
    rc = 0
    out = err = ''
    result = {
        'name': unit,
        'changed': False,
        'status': {
            
        },
        'warnings': [],
    }
    if module.params['daemon_reload']:
        (rc, out, err) = module.run_command(('%s daemon-reload' % systemctl))
        if (rc != 0):
            module.fail_json(msg=('failure %d during daemon-reload: %s' % (rc, err)))
    found = False
    is_initd = sysv_exists(unit)
    is_systemd = False
    (rc, out, err) = module.run_command(("%s show '%s'" % (systemctl, unit)))
    if (rc == 0):
        multival = []
        if out:
            k = None
            for line in to_native(out).split('\n'):
                if line.strip():
                    if (k is None):
                        if ('=' in line):
                            (k, v) = line.split('=', 1)
                            if v.lstrip().startswith('{'):
                                if (not v.rstrip().endswith('}')):
                                    multival.append(line)
                                    continue
                            result['status'][k] = v.strip()
                            k = None
                    elif line.rstrip().endswith('}'):
                        result['status'][k] = '\n'.join(multival).strip()
                        multival = []
                        k = None
                    else:
                        multival.append(line)
            is_systemd = (('LoadState' in result['status']) and (result['status']['LoadState'] != 'not-found'))
            if (is_systemd and ('LoadError' in result['status'])):
                module.fail_json(msg=("Error loading unit file '%s': %s" % (unit, result['status']['LoadError'])))
    found = (is_systemd or is_initd)
    if (is_initd and (not is_systemd)):
        result['warnings'].append(('The service (%s) is actually an init script but the system is managed by systemd' % unit))
    if (module.params['masked'] is not None):
        masked = (('LoadState' in result['status']) and (result['status']['LoadState'] == 'masked'))
        if (masked != module.params['masked']):
            result['changed'] = True
            if module.params['masked']:
                action = 'mask'
            else:
                action = 'unmask'
            if (not module.check_mode):
                (rc, out, err) = module.run_command(("%s %s '%s'" % (systemctl, action, unit)))
                if (rc != 0):
                    fail_if_missing(module, found, unit, msg='host')
    if (module.params['enabled'] is not None):
        if module.params['enabled']:
            action = 'enable'
        else:
            action = 'disable'
        fail_if_missing(module, found, unit, msg='host')
        enabled = False
        (rc, out, err) = module.run_command(("%s is-enabled '%s'" % (systemctl, unit)))
        if (rc == 0):
            enabled = True
        elif (rc == 1):
            if (is_initd and ((not out.startswith('disabled')) or sysv_is_enabled(unit))):
                enabled = True
        result['enabled'] = enabled
        if (enabled != module.params['enabled']):
            result['changed'] = True
            if (not module.check_mode):
                (rc, out, err) = module.run_command(("%s %s '%s'" % (systemctl, action, unit)))
                if (rc != 0):
                    module.fail_json(msg=('Unable to %s service %s: %s' % (action, unit, (out + err))))
            result['enabled'] = (not enabled)
    if (module.params['state'] is not None):
        fail_if_missing(module, found, unit, msg='host')
        result['state'] = module.params['state']
        if ('ActiveState' in result['status']):
            action = None
            if (module.params['state'] == 'started'):
                if (result['status']['ActiveState'] != 'active'):
                    action = 'start'
            elif (module.params['state'] == 'stopped'):
                if (result['status']['ActiveState'] == 'active'):
                    action = 'stop'
            else:
                if (result['status']['ActiveState'] != 'active'):
                    action = 'start'
                else:
                    action = module.params['state'][:(- 2)]
                result['state'] = 'started'
            if action:
                result['changed'] = True
                if (not module.check_mode):
                    (rc, out, err) = module.run_command(("%s %s '%s'" % (systemctl, action, unit)))
                    if (rc != 0):
                        module.fail_json(msg=('Unable to %s service %s: %s' % (action, unit, err)))
        else:
            module.fail_json(msg='Service is in unknown state', status=result['status'])
    module.exit_json(**result)