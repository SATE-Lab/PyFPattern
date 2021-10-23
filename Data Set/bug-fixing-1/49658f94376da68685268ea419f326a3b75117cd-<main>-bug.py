

def main():
    ' main entry point for module execution\n    '
    element_spec = dict(name=dict(), description=dict(), enabled=dict(default=True, type='bool'), speed=dict(), mtu=dict(type='int'), duplex=dict(choices=['full', 'half', 'auto']), tx_rate=dict(), rx_rate=dict(), delay=dict(default=10, type='int'), state=dict(default='present', choices=['present', 'absent', 'up', 'down']), active=dict(default=True, type='bool'))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['name'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(junos_argument_spec)
    required_one_of = [['name', 'aggregate']]
    mutually_exclusive = [['name', 'aggregate']]
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    top = 'interfaces/interface'
    param_to_xpath_map = collections.OrderedDict()
    param_to_xpath_map.update([('name', {
        'xpath': 'name',
        'is_key': True,
    }), ('description', 'description'), ('speed', 'speed'), ('mtu', 'mtu'), ('duplex', 'link-mode'), ('disable', {
        'xpath': 'disable',
        'tag_only': True,
    })])
    choice_to_value_map = {
        'link-mode': {
            'full': 'full-duplex',
            'half': 'half-duplex',
            'auto': 'automatic',
        },
    }
    params = to_param_list(module)
    requests = list()
    for param in params:
        for key in param:
            if (param.get(key) is None):
                param[key] = module.params[key]
        item = param.copy()
        state = item.get('state')
        item['disable'] = (True if (not item.get('enabled')) else False)
        if (state in ('present', 'up', 'down')):
            item['state'] = 'present'
        validate_param_values(module, param_to_xpath_map, param=item)
        want = map_params_to_obj(module, param_to_xpath_map, param=item)
        requests.append(map_obj_to_ele(module, want, top, value_map=choice_to_value_map, param=item))
    diff = None
    with locked_config(module):
        for req in requests:
            diff = load_config(module, tostring(req), warnings, action='merge')
        commit = (not module.check_mode)
        if diff:
            if commit:
                commit_configuration(module)
            else:
                discard_changes(module)
            result['changed'] = True
            if module._diff:
                result['diff'] = {
                    'prepared': diff,
                }
    failed_conditions = []
    for item in params:
        state = item.get('state')
        tx_rate = item.get('tx_rate')
        rx_rate = item.get('rx_rate')
        if ((state not in ('up', 'down')) and (tx_rate is None) and (rx_rate is None)):
            continue
        element = Element('get-interface-information')
        intf_name = SubElement(element, 'interface-name')
        intf_name.text = item.get('name')
        if result['changed']:
            sleep(item.get('delay'))
        reply = send_request(module, element, ignore_warning=False)
        if (state in ('up', 'down')):
            admin_status = reply.xpath('interface-information/physical-interface/admin-status')
            if ((not admin_status) or (not conditional(state, admin_status[0].text.strip()))):
                failed_conditions.append(('state ' + ('eq(%s)' % state)))
        if tx_rate:
            output_bps = reply.xpath('interface-information/physical-interface/traffic-statistics/output-bps')
            if ((not output_bps) or (not conditional(tx_rate, output_bps[0].text.strip(), cast=int))):
                failed_conditions.append(('tx_rate ' + tx_rate))
        if rx_rate:
            input_bps = reply.xpath('interface-information/physical-interface/traffic-statistics/input-bps')
            if ((not input_bps) or (not conditional(rx_rate, input_bps[0].text.strip(), cast=int))):
                failed_conditions.append(('rx_rate ' + rx_rate))
    if failed_conditions:
        msg = 'One or more conditional statements have not be satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)
    module.exit_json(**result)
