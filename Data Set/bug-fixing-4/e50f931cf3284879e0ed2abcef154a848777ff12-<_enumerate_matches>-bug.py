def _enumerate_matches(self, pattern):
    '\n        Returns a list of host names matching the given pattern according to the\n        rules explained above in _match_one_pattern.\n        '
    results = []
    matching_groups = self._match_list(self._inventory.groups, pattern)
    if matching_groups:
        for groupname in matching_groups:
            results.extend(self._inventory.groups[groupname].get_hosts())
    else:
        matching_hosts = self._match_list(self._inventory.hosts, pattern)
        if matching_hosts:
            for hostname in matching_hosts:
                results.append(self._inventory.hosts[hostname])
    if ((not results) and (pattern in C.LOCALHOST)):
        implicit = self._inventory.get_host(pattern)
        if implicit:
            results.append(implicit)
    if (not results):
        display.warning(('Could not match supplied host pattern, ignoring: %s' % pattern))
    return results