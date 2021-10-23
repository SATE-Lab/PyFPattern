def state_present(module, existing, commands):
    cmds = list()
    cmds.extend(commands)
    if (module.params['mode'] == 'maintenance'):
        cmds.insert(0, 'configure maintenance profile maintenance-mode')
    else:
        cmds.insert(0, 'configure maintenance profile normal-mode')
    return cmds