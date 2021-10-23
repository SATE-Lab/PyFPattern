def _needs_update(cloud, module, router, network, internal_subnet_ids):
    'Decide if the given router needs an update.\n    '
    if (router['admin_state_up'] != module.params['admin_state_up']):
        return True
    if router['external_gateway_info']:
        if (router['external_gateway_info'].get('enable_snat', True) != module.params['enable_snat']):
            return True
    if network:
        if (not router['external_gateway_info']):
            return True
        elif (router['external_gateway_info']['network_id'] != network['id']):
            return True
    if module.params['external_fixed_ips']:
        for new_iface in module.params['external_fixed_ips']:
            subnet = cloud.get_subnet(new_iface['subnet'])
            exists = False
            for existing_iface in router['external_gateway_info']['external_fixed_ips']:
                if (existing_iface['subnet_id'] == subnet['id']):
                    if ('ip' in new_iface):
                        if (existing_iface['ip_address'] == new_iface['ip']):
                            exists = True
                            break
                    else:
                        exists = True
                        break
            if (not exists):
                return True
    if module.params['interfaces']:
        existing_subnet_ids = []
        for port in cloud.list_router_interfaces(router, 'internal'):
            if ('fixed_ips' in port):
                for fixed_ip in port['fixed_ips']:
                    existing_subnet_ids.append(fixed_ip['subnet_id'])
        if (set(internal_subnet_ids) != set(existing_subnet_ids)):
            return True
    return False