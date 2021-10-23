

def injector():
    '\n    :rtype: list[str], dict[str, str]\n    '
    command = os.path.basename(__file__)
    executable = find_executable(command)
    if config.coverage_file:
        (args, env) = coverage_command()
    else:
        (args, env) = ([config.python_interpreter], os.environ.copy())
    args += [executable]
    if (command in ('ansible', 'ansible-playbook', 'ansible-pull')):
        if (config.remote_interpreter is None):
            interpreter = os.path.join(os.path.dirname(__file__), 'injector.py')
        elif (config.remote_interpreter == ''):
            interpreter = None
        else:
            interpreter = config.remote_interpreter
        if interpreter:
            args += ['--extra-vars', ('ansible_python_interpreter=' + interpreter)]
    args += config.arguments[1:]
    return (args, env)
