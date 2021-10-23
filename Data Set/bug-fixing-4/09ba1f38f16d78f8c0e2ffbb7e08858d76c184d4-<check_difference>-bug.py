def check_difference(self, **kwargs):
    'Check difference between action and user specified parameters.\n\n        Args:\n            **kwargs: Arbitrary keyword parameters.\n\n        Returns:\n            dict: dictionary of differences\n        '
    existing_action = convert_unicode_to_str(self._zapi_wrapper.check_if_action_exists(kwargs['name'])[0])
    parameters = convert_unicode_to_str(self._construct_parameters(**kwargs))
    change_parameters = {
        
    }
    _diff = cleanup_data(compare_dictionaries(parameters, existing_action, change_parameters))
    if (('recovery_operations' in cleanup_data(existing_action)) and ('acknowledge_operations' not in cleanup_data(parameters))):
        _diff['recovery_operations'] = []
    if (('acknowledge_operations' in cleanup_data(existing_action)) and ('acknowledge_operations' not in cleanup_data(parameters))):
        _diff['acknowledge_operations'] = []
    return _diff