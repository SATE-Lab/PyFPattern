def _add_arp_monitor(self, updates, key, want, have):
    commands = []
    arp_monitor = (updates.get(key) or {
        
    })
    diff_targets = self._get_arp_monitor_target_diff(want, have, key, 'target')
    if ('interval' in arp_monitor):
        commands.append(self._compute_command(key=(want['name'] + ' arp-monitor'), attrib='interval', value=str(arp_monitor['interval'])))
    if diff_targets:
        for target in diff_targets:
            commands.append(self._compute_command(key=(want['name'] + ' arp-monitor'), attrib='target', value=target))
    return commands