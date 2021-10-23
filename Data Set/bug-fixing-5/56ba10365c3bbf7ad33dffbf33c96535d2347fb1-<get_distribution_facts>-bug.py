def get_distribution_facts(self):
    self.facts['distribution_release'] = platform.release()
    self.facts['distribution_version'] = platform.version()
    systems_platform_working = ('NetBSD', 'FreeBSD')
    systems_implemented = ('AIX', 'HP-UX', 'Darwin', 'OpenBSD')
    if (self.system in systems_platform_working):
        pass
    elif (self.system in systems_implemented):
        self.facts['distribution'] = self.system
        cleanedname = self.system.replace('-', '')
        distfunc = getattr(self, ('get_distribution_' + cleanedname))
        distfunc()
    else:
        dist = platform.dist()
        self.facts['distribution'] = (dist[0].capitalize() or 'NA')
        self.facts['distribution_version'] = (dist[1] or 'NA')
        self.facts['distribution_major_version'] = (dist[1].split('.')[0] or 'NA')
        self.facts['distribution_release'] = (dist[2] or 'NA')
        for ddict in self.OSDIST_LIST:
            name = ddict['name']
            path = ddict['path']
            if (not os.path.exists(path)):
                continue
            if (os.path.getsize(path) == 0):
                if (('allowempty' in ddict) and ddict['allowempty']):
                    self.facts['distribution'] = name
                    break
                else:
                    continue
            data = get_file_content(path)
            if (name in self.SEARCH_STRING):
                if (self.SEARCH_STRING[name] in data):
                    self.facts['distribution'] = name
                else:
                    self.facts['distribution'] = data.split()[0]
                break
            else:
                distfunc = getattr(self, ('get_distribution_' + name))
                parsed = distfunc(name, data, path)
                if ((parsed is None) or parsed):
                    break
    self.facts['os_family'] = self.facts['distribution']
    distro = self.facts['distribution'].replace(' ', '_')
    if (distro in self.OS_FAMILY):
        self.facts['os_family'] = self.OS_FAMILY[distro]