def _add_hosts(self, hosts, group, hostnames):
    '\n            :param hosts: a list of hosts to be added to a group\n            :param group: the name of the group to which the hosts belong\n            :param hostnames: a list of hostname destination variables in order of preference\n        '
    for host in hosts:
        hostname = self._get_hostname(host, hostnames)
        host = camel_dict_to_snake_dict(host, ignore_list=['Tags'])
        host['tags'] = boto3_tag_list_to_ansible_dict(host.get('tags', []))
        if (not hostname):
            continue
        self.inventory.add_host(hostname, group=group)
        for (hostvar, hostval) in host.items():
            self.inventory.set_variable(hostname, hostvar, hostval)
        strict = self._options.get('strict', False)
        if self._options.get('compose'):
            self._set_composite_vars(self._options.get('compose'), host, hostname, strict=strict)
        if self._options.get('groups'):
            self._add_host_to_composed_groups(self._options.get('groups'), host, hostname, strict=strict)
        if self._options.get('keyed_groups'):
            self._add_host_to_keyed_groups(self._options.get('keyed_groups'), host, hostname, strict=strict)