def execute_show_command(command, module, command_type='cli_show'):
    if (module.params['transport'] == 'cli'):
        if ('show run' not in command):
            command += ' | json'
        cmds = [command]
        body = run_commands(module, cmds)
    elif (module.params['transport'] == 'nxapi'):
        cmds = [command]
        body = run_commands(module, cmds)
    return body