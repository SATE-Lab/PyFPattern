def main():
    ' Module main '
    argument_spec = dict(interface=dict(type='str'), vrid=dict(type='str'), virtual_ip=dict(type='str'), vrrp_type=dict(type='str', choices=['normal', 'member', 'admin']), admin_ignore_if_down=dict(type='str', choices=['true', 'false']), admin_vrid=dict(type='str'), admin_interface=dict(type='str'), admin_flowdown=dict(type='str', choices=['true', 'false']), priority=dict(type='str'), version=dict(type='str', choices=['v2', 'v3']), advertise_interval=dict(type='str'), preempt_timer_delay=dict(type='str'), gratuitous_arp_interval=dict(type='str'), recover_delay=dict(type='str'), holding_multiplier=dict(type='str'), auth_mode=dict(type='str', choices=['simple', 'md5', 'none']), is_plain=dict(type='str', choices=['true', 'false']), auth_key=dict(type='str'), fast_resume=dict(type='str', choices=['enable', 'disable']), state=dict(type='str', default='present', choices=['present', 'absent']))
    argument_spec.update(ce_argument_spec)
    module = Vrrp(argument_spec=argument_spec)
    module.work()