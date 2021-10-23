def main():
    module = AnsibleModule(argument_spec=dict(name=dict(), description=dict(), organization=dict(), scm_type=dict(choices=['manual', 'git', 'hg', 'svn'], default='manual'), scm_url=dict(), scm_branch=dict(), scm_credential=dict(), scm_clean=dict(type='bool', default=False), scm_delete_on_update=dict(type='bool', default=False), scm_update_on_launch=dict(type='bool', default=False), local_path=dict(), tower_host=dict(), tower_username=dict(), tower_password=dict(no_log=True), tower_verify_ssl=dict(type='bool', default=True), tower_config_file=dict(type='path'), state=dict(choices=['present', 'absent'], default='present')), supports_check_mode=True)
    if (not HAS_TOWER_CLI):
        module.fail_json(msg='ansible-tower-cli required for this module')
    name = module.params.get('name')
    description = module.params.get('description')
    organization = module.params.get('organization')
    scm_type = module.params.get('scm_type')
    if (scm_type == 'manual'):
        scm_type = ''
    scm_url = module.params.get('scm_url')
    local_path = module.params.get('local_path')
    scm_branch = module.params.get('scm_branch')
    scm_credential = module.params.get('scm_credential')
    scm_clean = module.params.get('scm_clean')
    scm_delete_on_update = module.params.get('scm_delete_on_update')
    scm_update_on_launch = module.params.get('scm_update_on_launch')
    state = module.params.get('state')
    json_output = {
        'project': name,
        'state': state,
    }
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        project = tower_cli.get_resource('project')
        try:
            if (state == 'present'):
                org_res = tower_cli.get_resource('organization')
                org = org_res.get(name=organization)
                result = project.modify(name=name, description=description, organization=org['id'], scm_type=scm_type, scm_url=scm_url, local_path=local_path, scm_branch=scm_branch, scm_clean=scm_clean, scm_credential=scm_credential, scm_delete_on_update=scm_delete_on_update, scm_update_on_launch=scm_update_on_launch, create_on_missing=True)
                json_output['id'] = result['id']
            elif (state == 'absent'):
                result = project.delete(name=name)
        except exc.NotFound as excinfo:
            module.fail_json(msg='Failed to update project, organization not found: {0}'.format(excinfo), changed=False)
        except (exc.ConnectionError, exc.BadRequest) as excinfo:
            module.fail_json(msg='Failed to update project: {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)