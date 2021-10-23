def populate_interfaces(self, interfaces):
    int_facts = dict()
    for interface in interfaces.findall('./data/interfaces/interface'):
        intf = dict()
        name = self.parse_item(interface, 'name')
        intf['description'] = self.parse_item(interface, 'description')
        intf['duplex'] = self.parse_item(interface, 'duplex')
        intf['primary_ipv4'] = self.parse_primary_ipv4(interface)
        intf['secondary_ipv4'] = self.parse_secondary_ipv4(interface)
        intf['ipv6'] = self.parse_ipv6_address(interface)
        intf['mtu'] = self.parse_item(interface, 'mtu')
        intf['type'] = self.parse_item(interface, 'type')
        int_facts[name] = intf
    for interface in interfaces.findall('./data/interfaces-state/interface'):
        name = self.parse_item(interface, 'name')
        intf = int_facts[name]
        intf['bandwidth'] = self.parse_item(interface, 'speed')
        intf['adminstatus'] = self.parse_item(interface, 'admin-status')
        intf['operstatus'] = self.parse_item(interface, 'oper-status')
        intf['macaddress'] = self.parse_item(interface, 'phys-address')
    for interface in interfaces.findall('./data/ports/ports-state/port'):
        name = self.parse_item(interface, 'name')
        mediatype = self.parse_item(interface, 'media-type')
        (typ, sname) = name.split('-eth')
        name = ('ethernet' + sname)
        try:
            intf = int_facts[name]
            intf['mediatype'] = mediatype
        except:
            for subport in xrange(1, 5):
                name = ((('ethernet' + sname) + ':') + str(subport))
                try:
                    intf = int_facts[name]
                    intf['mediatype'] = mediatype
                except:
                    pass
    return int_facts