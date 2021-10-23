def update_storage_system_pwd(module, ssid, pwd, api_url, api_usr, api_pwd):
    update_pwd = ('storage-systems/%s' % ssid)
    url = (api_url + update_pwd)
    post_body = json.dumps(dict(storedPassword=pwd))
    try:
        (rc, data) = request(url, data=post_body, method='POST', headers=HEADERS, url_username=api_usr, url_password=api_pwd)
    except Exception as e:
        module.fail_json(msg=('Failed to update system password. Id [%s].  Error [%s]' % (ssid, to_native(e))))
    return data