def update_volume(module, array):
    'Update Volume size and/or QoS'
    changed = False
    volfact = []
    api_version = array._list_available_rest_versions()
    vol = array.get_volume(module.params['name'])
    if (QOS_API_VERSION in api_version):
        vol_qos = array.get_volume(module.params['name'], qos=True)
        if (vol_qos['bandwidth_limit'] is None):
            vol_qos['bandwidth_limit'] = 0
    if module.params['size']:
        if (human_to_bytes(module.params['size']) != vol['size']):
            if (human_to_bytes(module.params['size']) > vol['size']):
                try:
                    volfact = array.extend_volume(module.params['name'], module.params['size'])
                    changed = True
                except Exception:
                    module.fail_json(msg='Volume {0} resize failed.'.format(module.params['name']))
    if (module.params['qos'] and (QOS_API_VERSION in api_version)):
        if (human_to_bytes(module.params['qos']) != vol_qos['bandwidth_limit']):
            if (module.params['qos'] == '0'):
                try:
                    volfact = array.set_volume(module.params['name'], bandwidth_limit='')
                    changed = True
                except Exception:
                    module.fail_json(msg='Volume {0} QoS removal failed.'.format(module.params['name']))
            elif (549755813888 >= int(human_to_bytes(module.params['qos'])) >= 1048576):
                try:
                    volfact = array.set_volume(module.params['name'], bandwidth_limit=module.params['qos'])
                    changed = True
                except Exception:
                    module.fail_json(msg='Volume {0} QoS change failed.'.format(module.params['name']))
            else:
                module.fail_json(msg='QoS value {0} out of range. Check documentation.'.format(module.params['qos']))
    module.exit_json(changed=changed, volume=volfact)