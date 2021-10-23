def handle_template(self, template, subdir):
    "\n        Determine where the app or project templates are.\n        Use django.__path__[0] as the default because the Django install\n        directory isn't known.\n        "
    if (template is None):
        return os.path.join(django.__path__[0], 'conf', subdir)
    else:
        if template.startswith('file://'):
            template = template[7:]
        expanded_template = os.path.expanduser(template)
        expanded_template = os.path.normpath(expanded_template)
        if os.path.isdir(expanded_template):
            return expanded_template
        if self.is_url(template):
            absolute_path = self.download(template)
        else:
            absolute_path = os.path.abspath(expanded_template)
        if os.path.exists(absolute_path):
            return self.extract(absolute_path)
    raise CommandError(("couldn't handle %s template %s." % (self.app_or_project, template)))