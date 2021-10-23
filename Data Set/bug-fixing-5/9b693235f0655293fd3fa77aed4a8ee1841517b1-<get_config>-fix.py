def get_config(parser, section, key, env_var, default_value, value_type=None, expand_relative_paths=False):
    ' kept for backwarsd compatibility, but deprecated '
    _deprecated('ansible.constants.get_config() is deprecated. There is new config API, see porting docs.')
    value = None
    value = os.environ.get(env_var, None)
    if (value is None):
        try:
            value = get_ini_config_value(parser, {
                'key': key,
                'section': section,
            })
        except:
            pass
    if (value is None):
        value = default_value
    value = ensure_type(value, value_type)
    return value