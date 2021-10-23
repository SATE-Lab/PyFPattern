def _fetch_information(token, url):
    try:
        response = open_url(url, headers={
            'X-Auth-Token': token,
            'Content-type': 'application/json',
        })
    except Exception:
        raise AnsibleError(('Error while fetching %s' % url))
    try:
        raw_json = json.loads(response.read())
    except ValueError:
        raise AnsibleError('Incorrect JSON payload')
    try:
        return raw_json['servers']
    except KeyError:
        raise AnsibleError('Incorrect format from the Scaleway API response')