def __init__(self, argument_spec):
    self.spec = argument_spec
    self.module = None
    self.init_module()
    self.interface = self.module.params['interface']
    self.mode = self.module.params['mode']
    self.state = self.module.params['state']
    self.access_vlan = self.module.params['access_vlan']
    self.native_vlan = self.module.params['native_vlan']
    self.trunk_vlans = self.module.params['trunk_vlans']
    self.host = self.module.params['host']
    self.username = self.module.params['username']
    self.port = self.module.params['port']
    self.changed = False
    self.updates_cmd = list()
    self.results = dict()
    self.proposed = dict()
    self.existing = dict()
    self.end_state = dict()
    self.intf_info = dict()
    self.intf_type = None