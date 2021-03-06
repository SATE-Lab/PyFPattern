def get(self, request, wizard_hash):
    '\n        This opens a page where with an active session fill stuff into the cache\n        Redirects to organization whenever cache has been deleted\n        '
    context = {
        'hash': wizard_hash,
    }
    key = ('%s%s' % (SETUP_WIZARD_CACHE_KEY, wizard_hash))
    wizard_data = default_cache.get(key)
    if (wizard_data is None):
        return self.redirect_to_org(request)
    orgs = client.get(reverse('sentry-api-0-organizations'), request=request)
    filled_projects = []
    for org in orgs.data:
        projects = client.get(reverse('sentry-api-0-organization-projects', kwargs={
            'organization_slug': org.get('slug'),
        }), request=request)
        for project in projects.data:
            if (project.get('status') == 'deleted'):
                continue
            enriched_project = project
            enriched_project['organization'] = org
            keys = client.get(reverse('sentry-api-0-project-keys', kwargs={
                'organization_slug': org.get('slug'),
                'project_slug': project.get('slug'),
            }), request=request)
            enriched_project['keys'] = keys.data
            filled_projects.append(enriched_project)
    token = None
    tokens = [x for x in ApiToken.objects.filter(user=request.user).all() if ('project:releases' in x.get_scopes())]
    if (not tokens):
        token = ApiToken.objects.create(user=request.user, scope_list=['project:releases'], refresh_token=None, expires_at=None)
    else:
        token = tokens[0]
    result = {
        'apiKeys': serialize(token),
        'projects': filled_projects,
    }
    key = ('%s%s' % (SETUP_WIZARD_CACHE_KEY, wizard_hash))
    default_cache.set(key, result, SETUP_WIZARD_CACHE_TIMEOUT)
    return render_to_response('sentry/setup-wizard.html', context, request)