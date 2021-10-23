def populate_neighbors(self, interfaces):
    for interface in interfaces.findall('./bulk/data/interface'):
        name = interface.find('name').text
        rem_sys_name = interface.find('./lldp-rem-neighbor-info/info/rem-system-name')
        if (rem_sys_name is not None):
            self.lldp_facts[name] = list()
            fact = dict()
            fact['host'] = rem_sys_name.text
            rem_sys_port = interface.find('./lldp-rem-neighbor-info/info/rem-lldp-port-id')
            fact['port'] = rem_sys_port.text
            self.lldp_facts[name].append(fact)