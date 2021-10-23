

def _parse(self, lines):
    '\n        Populates self.groups from the given array of lines. Raises an error on\n        any parse failure.\n        '
    self._compile_patterns()
    pending_declarations = {
        
    }
    groupname = 'ungrouped'
    state = 'hosts'
    self.lineno = 0
    for line in lines:
        self.lineno += 1
        line = line.strip()
        if ((not line) or (line[0] in self._COMMENT_MARKERS)):
            continue
        m = self.patterns['section'].match(line)
        if m:
            (groupname, state) = m.groups()
            state = (state or 'hosts')
            if (state not in ['hosts', 'children', 'vars']):
                title = ':'.join(m.groups())
                self._raise_error(('Section [%s] has unknown type: %s' % (title, state)))
            if (groupname not in self.groups):
                self.groups[groupname] = Group(name=groupname)
                if (state == 'vars'):
                    pending_declarations[groupname] = dict(line=self.lineno, state=state, name=groupname)
            if ((groupname in pending_declarations) and (state != 'vars')):
                del pending_declarations[groupname]
            continue
        elif (line.startswith('[') and line.endswith(']')):
            self._raise_error((("Invalid section entry: '%s'. Please make sure that there are no spaces" % line) + 'in the section entry, and that there are no other invalid characters'))
        if (state == 'hosts'):
            hosts = self._parse_host_definition(line)
            for h in hosts:
                self.groups[groupname].add_host(h)
            self.groups[groupname].get_hosts()
        elif (state == 'vars'):
            (k, v) = self._parse_variable_definition(line)
            self.groups[groupname].set_variable(k, v)
        elif (state == 'children'):
            child = self._parse_group_name(line)
            if (child not in self.groups):
                self.groups[child] = Group(name=child)
                pending_declarations[child] = dict(line=self.lineno, state=state, name=child, parent=groupname)
            self.groups[groupname].add_child_group(self.groups[child])
        else:
            self._raise_error(('Entered unhandled state: %s' % state))
    for g in pending_declarations:
        decl = pending_declarations[g]
        if (decl['state'] == 'vars'):
            raise AnsibleError(('%s:%d: Section [%s:vars] not valid for undefined group: %s' % (self.filename, decl['line'], decl['name'], decl['name'])))
        elif (decl['state'] == 'children'):
            raise AnsibleError(('%s:%d: Section [%s:children] includes undefined group: %s' % (self.filename, decl['line'], decl['parent'], decl['name'])))
    for group in self.groups.values():
        if ((group.depth == 0) and (group.name != 'all')):
            self.groups['all'].add_child_group(group)
