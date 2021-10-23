def _construct_url_3(self, root, parent, obj, child_includes):
    '\n        This method is used by get_url when the object is the third-level class.\n        '
    root_rn = root['aci_rn']
    root_obj = root['module_object']
    parent_class = parent['aci_class']
    parent_rn = parent['aci_rn']
    parent_filter = parent['filter_target']
    parent_obj = parent['module_object']
    obj_class = obj['aci_class']
    obj_rn = obj['aci_rn']
    obj_filter = obj['filter_target']
    obj = obj['module_object']
    if (not child_includes):
        self_child_includes = ('&rsp-subtree=full&rsp-subtree-class=' + obj_class)
    else:
        self_child_includes = '{},{}'.format(child_includes, obj_class)
    if (not child_includes):
        parent_self_child_includes = '&rsp-subtree=full&rsp-subtree-class={},{}'.format(parent_class, obj_class)
    else:
        parent_self_child_includes = '{},{},{}'.format(child_includes, parent_class, obj_class)
    if (self.module.params['state'] != 'query'):
        path = 'api/mo/uni/{}/{}/{}.json'.format(root_rn, parent_rn, obj_rn)
        filter_string = ('?rsp-prop-include=config-only' + child_includes)
    elif ((obj is None) and (parent_obj is None) and (root_obj is None)):
        path = 'api/class/{}.json'.format(obj_class)
        filter_string = ''
    elif (root_obj is not None):
        if (parent_obj is not None):
            if (obj is not None):
                path = 'api/mo/uni/{}/{}/{}.json'.format(root_rn, parent_rn, obj_rn)
                filter_string = ''
            else:
                path = 'api/mo/uni/{}/{}.json'.format(root_rn, parent_rn)
                filter_string = self_child_includes.replace('&', '?', 1)
        elif (obj is not None):
            path = 'api/mo/uni/{}.json'.format(root_rn)
            filter_string = '?rsp-subtree-filter=eq{}{}'.format(obj_filter, self_child_includes)
        else:
            path = 'api/mo/uni/{}.json'.format(root_rn)
            filter_string = ('?' + parent_self_child_includes)
    elif (parent_obj is not None):
        if (obj is not None):
            path = 'api/class/{}.json'.format(parent_class)
            filter_string = '?query-target-filter=eq{}{}&rsp-subtree-filter=eq{}'.format(parent_filter, self_child_includes, obj_filter)
        else:
            path = 'api/class/{}.json'.format(parent_class)
            filter_string = '?query-target-filter=eq{}{}'.format(parent_filter, self_child_includes)
    else:
        path = 'api/class/{}.json'.format(obj_class)
        filter_string = ('?query-target-filter=eq{}'.format(obj_filter) + child_includes)
    if ((child_includes is not None) and (filter_string == '')):
        filter_string = child_includes.replace('&', '?', 1)
    return (path, filter_string)