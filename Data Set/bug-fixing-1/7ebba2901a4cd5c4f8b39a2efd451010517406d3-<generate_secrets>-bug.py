

def generate_secrets(development=False):
    if development:
        OUTPUT_SETTINGS_FILENAME = 'zproject/dev-secrets.conf'
    else:
        OUTPUT_SETTINGS_FILENAME = '/etc/zulip/zulip-secrets.conf'
    current_conf = get_old_conf(OUTPUT_SETTINGS_FILENAME)
    lines = []
    if (len(current_conf) == 0):
        lines = ['[secrets]\n']

    def need_secret(name):
        return (name not in current_conf)

    def add_secret(name, value):
        lines.append(('%s = %s\n' % (name, value)))
        current_conf[name] = value
    for name in AUTOGENERATED_SETTINGS:
        if need_secret(name):
            add_secret(name, generate_random_token(64))
    if need_secret('secret_key'):
        add_secret('secret_key', generate_django_secretkey())
    if need_secret('camo_key'):
        add_secret('camo_key', get_random_string(64))
    if need_secret('zulip_org_key'):
        add_secret('zulip_org_key', get_random_string(64))
    if need_secret('zulip_org_id'):
        add_secret('zulip_org_id', str(uuid.uuid4()))
    if (not development):
        generate_camo_config_file(current_conf['camo_key'])
    if (len(lines) == 0):
        print('generate_secrets: No new secrets to generate.')
        return
    with open(OUTPUT_SETTINGS_FILENAME, 'a') as f:
        f.write(('\n' + ''.join(lines)))
    print(('Generated new secrets in %s.' % (OUTPUT_SETTINGS_FILENAME,)))
