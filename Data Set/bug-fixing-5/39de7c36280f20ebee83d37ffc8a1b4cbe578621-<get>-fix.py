def get(self, request):
    return self.respond({
        'name': 'Sentry',
        'description': 'Sentry',
        'key': JIRA_KEY,
        'baseUrl': absolute_uri(),
        'vendor': {
            'name': 'Sentry',
            'url': 'https://sentry.io',
        },
        'authentication': {
            'type': 'jwt',
        },
        'lifecycle': {
            'installed': '/extensions/jira/installed/',
            'uninstalled': '/extensions/jira/uninstalled/',
        },
        'apiVersion': 1,
        'modules': {
            'postInstallPage': {
                'url': '/extensions/jira/configure',
                'name': {
                    'value': 'Configure Sentry Add-on',
                },
                'key': 'post-install-sentry',
            },
            'configurePage': {
                'url': '/extensions/jira/configure',
                'name': {
                    'value': 'Configure Sentry Add-on',
                },
                'key': 'configure-sentry',
            },
            'webhooks': [{
                'event': 'jira:issue_updated',
                'url': reverse('sentry-extensions-jira-issue-updated'),
                'excludeBody': False,
            }],
        },
        'apiMigrations': {
            'gdpr': False,
        },
        'scopes': ['read', 'write', 'act_as_user'],
    })