

def get_sentry_sdk_config():
    return {
        'release': sentry.__build__,
        'environment': ENVIRONMENT,
        'in_app_include': ['sentry', 'sentry_plugins'],
        'debug': True,
        'send_default_pii': True,
    }
