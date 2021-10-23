

def __get_template_with_version(self):
    "\n        oVirt/RHV in version 4.1 doesn't support search by template+version_number,\n        so we need to list all templates with specific name and then iterate\n        through it's version until we find the version we look for.\n        "
    template = None
    templates_service = self._connection.system_service().templates_service()
    if self.param('template'):
        clusters_service = self._connection.system_service().clusters_service()
        cluster = search_by_name(clusters_service, self.param('cluster'))
        data_center = self._connection.follow_link(cluster.data_center)
        templates = templates_service.list(search=('name=%s and datacenter=%s' % (self.param('template'), data_center.name)))
        if self.param('template_version'):
            templates = [t for t in templates if (t.version.version_number == self.param('template_version'))]
        if (not templates):
            raise ValueError(("Template with name '%s' and version '%s' in data center '%s' was not found'" % (self.param('template'), self.param('template_version'), data_center.name)))
        template = sorted(templates, key=(lambda t: t.version.version_number), reverse=True)[0]
    elif self._is_new:
        template = templates_service.template_service('00000000-0000-0000-0000-000000000000').get()
    return template
