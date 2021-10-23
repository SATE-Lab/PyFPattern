def get_vars(self, play=None, host=None, task=None, include_hostvars=True, include_delegate_to=True, use_cache=True):
    '\n        Returns the variables, with optional "context" given via the parameters\n        for the play, host, and task (which could possibly result in different\n        sets of variables being returned due to the additional context).\n\n        The order of precedence is:\n        - play->roles->get_default_vars (if there is a play context)\n        - group_vars_files[host] (if there is a host context)\n        - host_vars_files[host] (if there is a host context)\n        - host->get_vars (if there is a host context)\n        - fact_cache[host] (if there is a host context)\n        - play vars (if there is a play context)\n        - play vars_files (if there\'s no host context, ignore\n          file names that cannot be templated)\n        - task->get_vars (if there is a task context)\n        - vars_cache[host] (if there is a host context)\n        - extra vars\n        '
    display.debug('in VariableManager get_vars()')
    all_vars = dict()
    magic_variables = self._get_magic_variables(play=play, host=host, task=task, include_hostvars=include_hostvars, include_delegate_to=include_delegate_to)
    if play:
        for role in play.get_roles():
            all_vars = combine_vars(all_vars, role.get_default_vars())
    if (task and (task._role is not None) and (play or (task.action == 'include_role'))):
        all_vars = combine_vars(all_vars, task._role.get_default_vars(dep_chain=task.get_dep_chain()))
    if host:
        basedir = self._loader.get_basedir()
        all_group = self._inventory.groups.get('all')
        host_groups = sort_groups([g for g in host.get_groups() if (g.name not in ['all'])])

        def _plugins_inventory(entities):
            ' merges all entities by inventory source '
            data = {
                
            }
            for inventory_dir in self._inventory._sources:
                if (',' in inventory_dir):
                    continue
                elif (not os.path.isdir(inventory_dir)):
                    inventory_dir = os.path.dirname(inventory_dir)
                for plugin in vars_loader.all():
                    data = combine_vars(data, plugin.get_vars(self._loader, inventory_dir, entities))
            return data

        def _plugins_play(entities):
            ' merges all entities adjacent to play '
            data = {
                
            }
            for plugin in vars_loader.all():
                data = combine_vars(data, plugin.get_vars(self._loader, basedir, entities))
            return data

        def all_inventory():
            return all_group.get_vars()

        def all_plugins_inventory():
            return _plugins_inventory([all_group])

        def all_plugins_play():
            return _plugins_play([all_group])

        def groups_inventory():
            ' gets group vars from inventory '
            return get_group_vars(host_groups)

        def groups_plugins_inventory():
            ' gets plugin sources from inventory for groups '
            return _plugins_inventory(host_groups)

        def groups_plugins_play():
            ' gets plugin sources from play for groups '
            return _plugins_play(host_groups)

        def plugins_by_groups():
            '\n                    merges all plugin sources by group,\n                    This should be used instead, NOT in combination with the other groups_plugins* functions\n                '
            data = {
                
            }
            for group in host_groups:
                data[group] = combine_vars(data[group], _plugins_inventory(group))
                data[group] = combine_vars(data[group], _plugins_play(group))
            return data
        for entry in C.VARIABLE_PRECEDENCE:
            if (entry.startswith('_') or ('.' in entry)):
                continue
            display.debug(('Calling %s to load vars for %s' % (entry, host.name)))
            all_vars = combine_vars(all_vars, locals()[entry]())
        all_vars = combine_vars(all_vars, host.get_vars())
        all_vars = combine_vars(all_vars, _plugins_inventory([host]))
        all_vars = combine_vars(all_vars, _plugins_play([host]))
        try:
            host_facts = wrap_var(self._fact_cache.get(host.name, dict()))
            if (not C.NAMESPACE_FACTS):
                all_vars = combine_vars(all_vars, host_facts)
            all_vars = combine_vars(all_vars, {
                'ansible_facts': host_facts,
            })
        except KeyError:
            pass
    if play:
        all_vars = combine_vars(all_vars, play.get_vars())
        for vars_file_item in play.get_vars_files():
            temp_vars = combine_vars(all_vars, self._extra_vars)
            temp_vars = combine_vars(temp_vars, magic_variables)
            templar = Templar(loader=self._loader, variables=temp_vars)
            vars_file_list = vars_file_item
            if (not isinstance(vars_file_list, list)):
                vars_file_list = [vars_file_list]
            try:
                for vars_file in vars_file_list:
                    vars_file = templar.template(vars_file)
                    try:
                        data = preprocess_vars(self._loader.load_from_file(vars_file, unsafe=True))
                        if (data is not None):
                            for item in data:
                                all_vars = combine_vars(all_vars, item)
                        break
                    except AnsibleFileNotFound:
                        continue
                    except AnsibleParserError:
                        raise
                else:
                    if include_delegate_to:
                        raise AnsibleFileNotFound(('vars file %s was not found' % vars_file_item))
            except (UndefinedError, AnsibleUndefinedVariable):
                if ((host is not None) and self._fact_cache.get(host.name, dict()).get('module_setup') and (task is not None)):
                    raise AnsibleUndefinedVariable(("an undefined variable was found when attempting to template the vars_files item '%s'" % vars_file_item), obj=vars_file_item)
                else:
                    display.vvv(("skipping vars_file '%s' due to an undefined variable" % vars_file_item))
                    continue
        if (not C.DEFAULT_PRIVATE_ROLE_VARS):
            for role in play.get_roles():
                all_vars = combine_vars(all_vars, role.get_vars(include_params=False))
    if task:
        if task._role:
            all_vars = combine_vars(all_vars, task._role.get_vars(task.get_dep_chain(), include_params=False))
        all_vars = combine_vars(all_vars, task.get_vars())
    if host:
        all_vars = combine_vars(all_vars, self._vars_cache.get(host.get_name(), dict()))
        all_vars = combine_vars(all_vars, self._nonpersistent_fact_cache.get(host.name, dict()))
    if task:
        if task._role:
            all_vars = combine_vars(all_vars, task._role.get_role_params(task.get_dep_chain()))
        all_vars = combine_vars(all_vars, task.get_include_params())
    all_vars = combine_vars(all_vars, self._extra_vars)
    all_vars = combine_vars(all_vars, magic_variables)
    if task:
        all_vars['environment'] = task.environment
    if (task and (task.delegate_to is not None) and include_delegate_to):
        all_vars['ansible_delegated_vars'] = self._get_delegated_vars(play, task, all_vars)
    if (task or play):
        all_vars['vars'] = all_vars.copy()
    display.debug('done with get_vars()')
    return all_vars