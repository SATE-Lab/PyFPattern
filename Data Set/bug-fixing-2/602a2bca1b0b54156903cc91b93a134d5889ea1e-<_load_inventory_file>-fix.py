

def _load_inventory_file(self, path, loader, filter_ext=False):
    '\n        helper function, which loads the file and gets the\n        basename of the file without the extension\n        '
    if loader.is_directory(path):
        data = dict()
        try:
            names = loader.list_directory(path)
        except os.error as err:
            raise AnsibleError(('This folder cannot be listed: %s: %s.' % (path, err.strerror)))
        names.sort()
        paths = [os.path.join(path, name) for name in names if (not (name.startswith('.') or name.endswith('~')))]
        for p in paths:
            results = self._load_inventory_file(path=p, loader=loader, filter_ext=True)
            if (results is not None):
                data = combine_vars(data, results)
    else:
        (file_name, ext) = os.path.splitext(path)
        data = None
        if ((not filter_ext) or (ext in C.YAML_FILENAME_EXTENSIONS)):
            if loader.path_exists(path):
                data = loader.load_from_file(path)
            else:
                for test_ext in (ext for ext in C.YAML_FILENAME_EXTENSIONS if ext):
                    new_path = (path + test_ext)
                    if loader.path_exists(new_path):
                        data = loader.load_from_file(new_path)
                        break
    rval = AnsibleInventoryVarsData()
    rval.path = path
    if (data is not None):
        if (not isinstance(data, dict)):
            raise AnsibleError(("Problem parsing file '%s': line %d, column %d" % data.ansible_pos))
        else:
            rval.update(data)
    return rval
