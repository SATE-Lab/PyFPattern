@staticmethod
def load(data, play, current_role_path=None, parent_role=None, variable_manager=None, loader=None):
    if (not (isinstance(data, string_types) or isinstance(data, dict) or isinstance(data, AnsibleBaseYAMLObject))):
        raise AnsibleParserError(('Invalid role definition: %s' % to_native(data)))
    if (isinstance(data, string_types) and (',' in data)):
        data = RoleRequirement.role_spec_parse(data)
    ri = RoleInclude(play=play, role_basedir=current_role_path, variable_manager=variable_manager, loader=loader)
    return ri.load_data(data, variable_manager=variable_manager, loader=loader)