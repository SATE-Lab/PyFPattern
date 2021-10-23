

def main():
    'Ansible Main module.'
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), architecture=dict(type='str'), config=dict(type='dict'), devices=dict(type='dict'), ephemeral=dict(type='bool'), profiles=dict(type='list'), source=dict(type='dict'), state=dict(choices=LXD_ANSIBLE_STATES.keys(), default='started'), timeout=dict(type='int', default=30), wait_for_ipv4_addresses=dict(type='bool', default=False), force_stop=dict(type='bool', default=False), url=dict(type='str', default='unix:/var/lib/lxd/unix.socket'), key_file=dict(type='str', default='{}/.config/lxc/client.key'.format(os.environ['HOME'])), cert_file=dict(type='str', default='{}/.config/lxc/client.crt'.format(os.environ['HOME'])), trust_password=dict(type='str', no_log=True)), supports_check_mode=False)
    lxd_manage = LXDContainerManagement(module=module)
    lxd_manage.run()
