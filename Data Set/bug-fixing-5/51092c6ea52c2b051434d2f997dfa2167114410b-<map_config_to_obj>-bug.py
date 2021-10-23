def map_config_to_obj(module):
    config = get_config(module, flags=['| section interface'])
    configobj = NetworkConfig(indent=3, contents=config)
    match = re.findall('^interface (\\S+)', config, re.M)
    if (not match):
        return list()
    instances = list()
    for item in set(match):
        command = 'sh int {0} switchport | include Switchport'
        switchport_cfg = run_commands(module, command.format(item))[0].split(':')[1].strip()
        if (switchport_cfg == 'Enabled'):
            state = 'present'
        else:
            state = 'absent'
        obj = {
            'name': item.lower(),
            'state': state,
        }
        obj['access_vlan'] = parse_config_argument(configobj, item, 'switchport access vlan')
        obj['native_vlan'] = parse_config_argument(configobj, item, 'switchport trunk native vlan')
        obj['trunk_allowed_vlans'] = parse_config_argument(configobj, item, 'switchport trunk allowed vlan')
        if obj['access_vlan']:
            obj['mode'] = 'access'
        else:
            obj['mode'] = 'trunk'
        instances.append(obj)
    return instances