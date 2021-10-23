def generate_commands(vlan_id, to_set, to_remove):
    commands = []
    if ('vlan_id' in to_remove):
        return ['no vlan {0}'.format(vlan_id)]
    for (key, value) in to_set.items():
        if (value is None):
            continue
        commands.append('{0} {1}'.format(key, value))
    for key in to_remove:
        commands.append('no {0}'.format(key))
    if commands:
        commands.insert(0, 'vlan {0}'.format(vlan_id))
    return commands