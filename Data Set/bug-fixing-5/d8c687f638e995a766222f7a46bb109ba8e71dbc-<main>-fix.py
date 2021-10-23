def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), arn=dict(required=False, type='str'), family=dict(required=False, type='str'), revision=dict(required=False, type='int'), force_create=dict(required=False, default=False, type='bool'), containers=dict(required=False, type='list'), network_mode=dict(required=False, default='bridge', choices=['bridge', 'host', 'none', 'awsvpc'], type='str'), task_role_arn=dict(required=False, default='', type='str'), execution_role_arn=dict(required=False, default='', type='str'), volumes=dict(required=False, type='list'), launch_type=dict(required=False, choices=['EC2', 'FARGATE']), cpu=dict(), memory=dict(required=False, type='str')))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[('launch_type', 'FARGATE', ['cpu', 'memory'])])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    task_to_describe = None
    task_mgr = EcsTaskManager(module)
    results = dict(changed=False)
    if module.params['launch_type']:
        if (not module.botocore_at_least('1.8.4')):
            module.fail_json(msg='botocore needs to be version 1.8.4 or higher to use launch_type')
    if module.params['execution_role_arn']:
        if (not module.botocore_at_least('1.10.44')):
            module.fail_json(msg='botocore needs to be version 1.10.44 or higher to use execution_role_arn')
    if module.params['containers']:
        for container in module.params['containers']:
            for environment in container.get('environment', []):
                environment['value'] = to_text(environment['value'])
    if (module.params['state'] == 'present'):
        if (('containers' not in module.params) or (not module.params['containers'])):
            module.fail_json(msg='To use task definitions, a list of containers must be specified')
        if (('family' not in module.params) or (not module.params['family'])):
            module.fail_json(msg='To use task definitions, a family must be specified')
        network_mode = module.params['network_mode']
        launch_type = module.params['launch_type']
        if ((launch_type == 'FARGATE') and (network_mode != 'awsvpc')):
            module.fail_json(msg='To use FARGATE launch type, network_mode must be awsvpc')
        family = module.params['family']
        existing_definitions_in_family = task_mgr.describe_task_definitions(module.params['family'])
        if (('revision' in module.params) and module.params['revision']):
            revision = int(module.params['revision'])
            tasks_defs_for_revision = [td for td in existing_definitions_in_family if (td['revision'] == revision)]
            existing = (tasks_defs_for_revision[0] if (len(tasks_defs_for_revision) > 0) else None)
            if (existing and (existing['status'] != 'ACTIVE')):
                module.fail_json(msg=("A task in family '%s' already exists for revsion %d, but it is inactive" % (family, revision)))
            elif (not existing):
                if ((not existing_definitions_in_family) and (revision != 1)):
                    module.fail_json(msg=('You have specified a revision of %d but a created revision would be 1' % revision))
                elif (existing_definitions_in_family and ((existing_definitions_in_family[(- 1)]['revision'] + 1) != revision)):
                    module.fail_json(msg=('You have specified a revision of %d but a created revision would be %d' % (revision, (existing_definitions_in_family[(- 1)]['revision'] + 1))))
        else:
            existing = None

            def _right_has_values_of_left(left, right):
                for (k, v) in left.items():
                    if (not (((not v) and ((k not in right) or (not right[k]))) or ((k in right) and (v == right[k])))):
                        if (isinstance(v, list) and (k in right)):
                            left_list = v
                            right_list = (right[k] or [])
                            if (len(left_list) != len(right_list)):
                                return False
                            for list_val in left_list:
                                if (list_val not in right_list):
                                    return False
                        else:
                            return False
                for (k, v) in right.items():
                    if (v and (k not in left)):
                        return False
                return True

            def _task_definition_matches(requested_volumes, requested_containers, requested_task_role_arn, existing_task_definition):
                if (td['status'] != 'ACTIVE'):
                    return None
                if (requested_task_role_arn != td.get('taskRoleArn', '')):
                    return None
                existing_volumes = (td.get('volumes', []) or [])
                if (len(requested_volumes) != len(existing_volumes)):
                    return None
                if (len(requested_volumes) > 0):
                    for requested_vol in requested_volumes:
                        found = False
                        for actual_vol in existing_volumes:
                            if _right_has_values_of_left(requested_vol, actual_vol):
                                found = True
                                break
                        if (not found):
                            return None
                existing_containers = (td.get('containerDefinitions', []) or [])
                if (len(requested_containers) != len(existing_containers)):
                    return None
                for requested_container in requested_containers:
                    found = False
                    for actual_container in existing_containers:
                        if _right_has_values_of_left(requested_container, actual_container):
                            found = True
                            break
                    if (not found):
                        return None
                return existing_task_definition
            for td in existing_definitions_in_family:
                requested_volumes = (module.params['volumes'] or [])
                requested_containers = (module.params['containers'] or [])
                requested_task_role_arn = module.params['task_role_arn']
                existing = _task_definition_matches(requested_volumes, requested_containers, requested_task_role_arn, td)
                if existing:
                    break
        if (existing and (not module.params.get('force_create'))):
            results['taskdefinition'] = existing
        else:
            if (not module.check_mode):
                volumes = (module.params.get('volumes', []) or [])
                results['taskdefinition'] = task_mgr.register_task(module.params['family'], module.params['task_role_arn'], module.params['execution_role_arn'], module.params['network_mode'], module.params['containers'], volumes, module.params['launch_type'], module.params['cpu'], module.params['memory'])
            results['changed'] = True
    elif (module.params['state'] == 'absent'):
        if (module.params['state'] == 'absent'):
            if (('arn' in module.params) and (module.params['arn'] is not None)):
                task_to_describe = module.params['arn']
            elif (('family' in module.params) and (module.params['family'] is not None) and ('revision' in module.params) and (module.params['revision'] is not None)):
                task_to_describe = ((module.params['family'] + ':') + str(module.params['revision']))
            else:
                module.fail_json(msg='To use task definitions, an arn or family and revision must be specified')
        existing = task_mgr.describe_task(task_to_describe)
        if (not existing):
            pass
        else:
            results['taskdefinition'] = existing
            if (('status' in existing) and (existing['status'] == 'INACTIVE')):
                results['changed'] = False
            else:
                if (not module.check_mode):
                    task_mgr.deregister_task(task_to_describe)
                results['changed'] = True
    module.exit_json(**results)