def get_sflow_dict(self):
    ' sflow config dict'
    sflow_dict = dict(source=list(), agent=dict(), collector=list(), sampling=dict(), counter=dict(), export=dict())
    conf_str = (CE_NC_GET_SFLOW % (self.sflow_interface, self.sflow_interface))
    if (not self.collector_meth):
        conf_str = conf_str.replace('<meth></meth>', '')
    rcv_xml = self.netconf_get_config(conf_str)
    if ('<data/>' in rcv_xml):
        return sflow_dict
    xml_str = rcv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    srcs = root.findall('sflow/sources/source')
    if srcs:
        for src in srcs:
            attrs = dict()
            for attr in src:
                if (attr.tag in ['family', 'ipv4Addr', 'ipv6Addr']):
                    attrs[attr.tag] = attr.text
            sflow_dict['source'].append(attrs)
    agent = root.find('sflow/agents/agent')
    if agent:
        for attr in agent:
            if (attr.tag in ['family', 'ipv4Addr', 'ipv6Addr']):
                sflow_dict['agent'][attr.tag] = attr.text
    collectors = root.findall('sflow/collectors/collector')
    if collectors:
        for collector in collectors:
            attrs = dict()
            for attr in collector:
                if (attr.tag in ['collectorID', 'family', 'ipv4Addr', 'ipv6Addr', 'vrfName', 'datagramSize', 'port', 'description', 'meth']):
                    attrs[attr.tag] = attr.text
            sflow_dict['collector'].append(attrs)
    sample = root.find('sflow/samplings/sampling')
    if sample:
        for attr in sample:
            if (attr.tag in ['ifName', 'collectorID', 'direction', 'length', 'rate']):
                sflow_dict['sampling'][attr.tag] = attr.text
    counter = root.find('sflow/counters/counter')
    if counter:
        for attr in counter:
            if (attr.tag in ['ifName', 'collectorID', 'interval']):
                sflow_dict['counter'][attr.tag] = attr.text
    export = root.find('sflow/exports/export')
    if export:
        for attr in export:
            if (attr.tag == 'ExportRoute'):
                sflow_dict['export'][attr.tag] = attr.text
    return sflow_dict