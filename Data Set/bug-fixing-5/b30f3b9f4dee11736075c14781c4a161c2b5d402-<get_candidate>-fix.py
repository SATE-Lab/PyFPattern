def get_candidate(module):
    candidate = NetworkConfig(indent=3)
    if module.params['src']:
        candidate.load(module.params['src'])
    elif module.params['lines']:
        parents = (module.params['parents'] or list())
        candidate.add(module.params['lines'], parents=parents)
    return candidate