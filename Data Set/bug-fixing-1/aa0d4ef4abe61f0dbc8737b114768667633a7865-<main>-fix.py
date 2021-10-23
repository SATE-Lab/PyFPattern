

def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent', 'exported', 'imported', 'registered'], default='present'), id=dict(default=None), name=dict(default=None), vm=dict(default=None), timezone=dict(type='str'), description=dict(default=None), sso=dict(type='bool'), ballooning_enabled=dict(type='bool', default=None), cluster=dict(default=None), usb_support=dict(type='bool'), allow_partial_import=dict(default=None, type='bool'), cpu_profile=dict(default=None), clone_permissions=dict(type='bool'), export_domain=dict(default=None), storage_domain=dict(default=None), exclusive=dict(type='bool'), clone_name=dict(default=None), image_provider=dict(default=None), soundcard_enabled=dict(type='bool', default=None), smartcard_enabled=dict(type='bool', default=None), image_disk=dict(default=None, aliases=['glance_image_disk_name']), io_threads=dict(type='int', default=None), template_image_disk_name=dict(default=None), version=dict(default=None, type='dict'), seal=dict(type='bool'), vnic_profile_mappings=dict(default=[], type='list'), cluster_mappings=dict(default=[], type='list'), role_mappings=dict(default=[], type='list'), domain_mappings=dict(default=[], type='list'), operating_system=dict(type='str'), memory=dict(type='str'), memory_guaranteed=dict(type='str'), memory_max=dict(type='str'), nics=dict(type='list', default=[]), cloud_init=dict(type='dict'), cloud_init_nics=dict(type='list', default=[]), sysprep=dict(type='dict'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=[['id', 'name']])
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        templates_service = connection.system_service().templates_service()
        templates_module = TemplatesModule(connection=connection, module=module, service=templates_service)
        entity = None
        if ((module.params['version'] is not None) and (module.params['version'].get('number') is not None)):
            entity = find_subversion_template(module, templates_service)
        state = module.params['state']
        if (state == 'present'):
            force_create = False
            if ((entity is None) and (module.params['version'] is not None)):
                force_create = True
            ret = templates_module.create(entity=entity, force_create=force_create, result_state=otypes.TemplateStatus.OK, search_params=searchable_attributes(module), clone_permissions=module.params['clone_permissions'], seal=module.params['seal'])
        elif (state == 'absent'):
            ret = templates_module.remove(entity=entity)
        elif (state == 'exported'):
            template = templates_module.search_entity()
            if (entity is not None):
                template = entity
            export_service = templates_module._get_export_domain_service()
            export_template = search_by_attributes(export_service.templates_service(), id=template.id)
            ret = templates_module.action(entity=template, action='export', action_condition=(lambda t: ((export_template is None) or module.params['exclusive'])), wait_condition=(lambda t: (t is not None)), post_action=templates_module.post_export_action, storage_domain=otypes.StorageDomain(id=export_service.get().id), exclusive=module.params['exclusive'])
        elif (state == 'imported'):
            template = templates_module.search_entity()
            if (entity is not None):
                template = entity
            if (template and (module.params['clone_name'] is None)):
                ret = templates_module.create(result_state=otypes.TemplateStatus.OK)
            else:
                kwargs = {
                    
                }
                if module.params['image_provider']:
                    kwargs.update(disk=otypes.Disk(name=(module.params['template_image_disk_name'] or module.params['image_disk'])), template=otypes.Template(name=(module.params['name'] if (module.params['clone_name'] is None) else module.params['clone_name'])), clone=(True if (module.params['clone_name'] is not None) else False), import_as_template=True)
                if module.params['image_disk']:
                    templates_module._get_export_domain_service().images_service().list()
                    glance_service = connection.system_service().openstack_image_providers_service()
                    image_provider = search_by_name(glance_service, module.params['image_provider'])
                    images_service = glance_service.service(image_provider.id).images_service()
                else:
                    images_service = templates_module._get_export_domain_service().templates_service()
                template_name = (module.params['image_disk'] or module.params['name'])
                entity = search_by_name(images_service, template_name)
                if (entity is None):
                    raise Exception(("Image/template '%s' was not found." % template_name))
                images_service.service(entity.id).import_(storage_domain=(otypes.StorageDomain(name=module.params['storage_domain']) if module.params['storage_domain'] else None), cluster=(otypes.Cluster(name=module.params['cluster']) if module.params['cluster'] else None), **kwargs)
                template = templates_module.wait_for_import(condition=(lambda t: (t.status == otypes.TemplateStatus.OK)))
                if (template is None):
                    raise TimeoutError(("Image/template '%s' could not be imported. Try again with larger timeout." % template_name))
                ret = templates_module.create(result_state=otypes.TemplateStatus.OK)
        elif (state == 'registered'):
            storage_domains_service = connection.system_service().storage_domains_service()
            sd_id = get_id_by_name(storage_domains_service, module.params['storage_domain'])
            storage_domain_service = storage_domains_service.storage_domain_service(sd_id)
            templates_service = storage_domain_service.templates_service()
            templates = templates_service.list(unregistered=True)
            template = next((t for t in templates if ((t.id == module.params['id']) or (t.name == module.params['name']))), None)
            changed = False
            if (template is None):
                template = templates_module.search_entity()
                if (template is None):
                    raise ValueError(("Template '%s(%s)' wasn't found." % (module.params['name'], module.params['id'])))
            else:
                changed = True
                template_service = templates_service.template_service(template.id)
                template_service.register(allow_partial_import=module.params['allow_partial_import'], cluster=(otypes.Cluster(name=module.params['cluster']) if module.params['cluster'] else None), vnic_profile_mappings=(_get_vnic_profile_mappings(module) if module.params['vnic_profile_mappings'] else None), registration_configuration=(otypes.RegistrationConfiguration(cluster_mappings=_get_cluster_mappings(module), role_mappings=_get_role_mappings(module), domain_mappings=_get_domain_mappings(module)) if (module.params['cluster_mappings'] or module.params['role_mappings'] or module.params['domain_mappings']) else None))
                if module.params['wait']:
                    template = templates_module.wait_for_import()
                else:
                    template = template_service.get()
                ret = templates_module.create(result_state=otypes.TemplateStatus.OK)
            ret = {
                'changed': changed,
                'id': template.id,
                'template': get_dict_of_struct(template),
            }
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))
