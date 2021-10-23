def _get_hostgroup_vars(self, host=None, group=None, new_pb_basedir=False):
    '\n        Loads variables from group_vars/<groupname> and host_vars/<hostname> in directories parallel\n        to the inventory base directory or in the same directory as the playbook.  Variables in the playbook\n        dir will win over the inventory dir if files are in both.\n        '
    results = {
        
    }
    scan_pass = 0
    _basedir = self._basedir
    _playbook_basedir = self._playbook_basedir
    if (not new_pb_basedir):
        basedirs = [_basedir, _playbook_basedir]
    else:
        basedirs = [_playbook_basedir]
    for basedir in basedirs:
        if (basedir in ('', None)):
            basedir = './'
        scan_pass = (scan_pass + 1)
        if (not os.path.exists(basedir)):
            continue
        if ((_basedir == _playbook_basedir) and (scan_pass != 1)):
            continue
        if ((host is None) and any(map((lambda ext: ((group.name + ext) in self._group_vars_files)), C.YAML_FILENAME_EXTENSIONS))):
            base_path = to_unicode(os.path.abspath(os.path.join(to_bytes(basedir), (b'group_vars/' + to_bytes(group.name)))), errors='strict')
            results = combine_vars(results, self._variable_manager.add_group_vars_file(base_path, self._loader))
        elif ((group is None) and any(map((lambda ext: ((host.name + ext) in self._host_vars_files)), C.YAML_FILENAME_EXTENSIONS))):
            base_path = to_unicode(os.path.abspath(os.path.join(to_bytes(basedir), (b'host_vars/' + to_bytes(host.name)))), errors='strict')
            results = combine_vars(results, self._variable_manager.add_host_vars_file(base_path, self._loader))
    return results