@ensure_connected
def get_configuration(self, format='xml', filter=None):
    '\n        Retrieve all or part of a specified configuration.\n        :param format: format in which configuration should be retrieved\n        :param filter: specifies the portion of the configuration to retrieve\n               as either xml string rooted in <configuration> element\n        :return: Received rpc response from remote host in string format\n        '
    if (filter is not None):
        if (not isinstance(filter, string_types)):
            raise AnsibleConnectionFailure(("get configuration filter should be of type string, received value '%s' is of type '%s'" % (filter, type(filter))))
        filter = to_ele(filter)
    return self.m.get_configuration(format=format, filter=filter).data_xml