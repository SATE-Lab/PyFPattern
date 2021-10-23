def __init__(self, module):
    self.module = module
    self.dv_switch = None
    self.uplink_portgroup = None
    self.host = None
    self.dv_switch = None
    self.nic = None
    self.content = connect_to_api(self.module)
    self.state = self.module.params['state']
    self.switch_name = self.module.params['switch_name']
    self.esxi_hostname = self.module.params['esxi_hostname']
    self.vmnics = self.module.params['vmnics']