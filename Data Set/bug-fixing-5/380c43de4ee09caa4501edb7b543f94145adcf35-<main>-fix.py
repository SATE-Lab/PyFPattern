def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(stack_name=dict(), all_facts=dict(required=False, default=False, type='bool'), stack_policy=dict(required=False, default=False, type='bool'), stack_events=dict(required=False, default=False, type='bool'), stack_resources=dict(required=False, default=False, type='bool'), stack_template=dict(required=False, default=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    service_mgr = CloudFormationServiceManager(module)
    result = {
        'ansible_facts': {
            'cloudformation': {
                
            },
        },
    }
    for stack_description in service_mgr.describe_stacks(module.params.get('stack_name')):
        facts = {
            'stack_description': stack_description,
        }
        stack_name = stack_description.get('StackName')
        if facts['stack_description']:
            facts['stack_outputs'] = to_dict(facts['stack_description'].get('Outputs'), 'OutputKey', 'OutputValue')
            facts['stack_parameters'] = to_dict(facts['stack_description'].get('Parameters'), 'ParameterKey', 'ParameterValue')
            facts['stack_tags'] = boto3_tag_list_to_ansible_dict(facts['stack_description'].get('Tags'))
        facts['stack_description'] = camel_dict_to_snake_dict(facts['stack_description'])
        all_facts = module.params.get('all_facts')
        if (all_facts or module.params.get('stack_resources')):
            facts['stack_resource_list'] = service_mgr.list_stack_resources(stack_name)
            facts['stack_resources'] = to_dict(facts.get('stack_resource_list'), 'LogicalResourceId', 'PhysicalResourceId')
        if (all_facts or module.params.get('stack_template')):
            facts['stack_template'] = service_mgr.get_template(stack_name)
        if (all_facts or module.params.get('stack_policy')):
            facts['stack_policy'] = service_mgr.get_stack_policy(stack_name)
        if (all_facts or module.params.get('stack_events')):
            facts['stack_events'] = service_mgr.describe_stack_events(stack_name)
        result['ansible_facts']['cloudformation'][stack_name] = facts
    result['changed'] = False
    module.exit_json(**result)