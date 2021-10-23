

def _new_order_v2(self):
    '\n        Start a new certificate order (ACME v2 protocol).\n        https://tools.ietf.org/html/draft-ietf-acme-acme-09#section-7.4\n        '
    identifiers = []
    for domain in self.domains:
        identifiers.append({
            'type': 'dns',
            'value': domain,
        })
    new_order = {
        'identifiers': identifiers,
    }
    (result, info) = self.account.send_signed_request(self.directory['newOrder'], new_order)
    if (info['status'] not in [201]):
        raise ModuleFailException('Error new order: CODE: {0} RESULT: {1}'.format(info['status'], result))
    for auth_uri in result['authorizations']:
        auth_data = simple_get(self.module, auth_uri)
        auth_data['uri'] = auth_uri
        domain = auth_data['identifier']['value']
        if auth_data.get('wildcard', False):
            domain = '*.{0}'.format(domain)
        self.authorizations[domain] = auth_data
    self.order_uri = info['location']
    self.finalize_uri = result['finalize']
