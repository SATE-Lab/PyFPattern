def __init__(self, module):
    self.module = module
    self.dvs = None
    self.switch_name = self.module.params['switch_name']
    self.datacenter_name = self.module.params['datacenter_name']
    self.mtu = self.module.params['mtu']
    self.uplink_quantity = self.module.params['uplink_quantity']
    self.discovery_proto = self.module.params['discovery_proto']
    self.discovery_operation = self.module.params['discovery_operation']
    self.state = self.module.params['state']
    self.content = connect_to_api(module)